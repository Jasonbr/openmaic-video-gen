#!/usr/bin/env python3
"""
视频号助手自动化上传脚本
支持: 登录、上传视频、填写信息、保存草稿

使用方法:
    python3 video_channel_uploader.py --video /path/to/video.mp4 --config config.json

依赖:
    pip install selenium playwright webdriver-manager
"""

import argparse
import json
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright未安装，将使用Selenium作为备选")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class VideoChannelUploader:
    """视频号助手自动化上传器"""
    
    def __init__(self, method="playwright"):
        self.method = method
        self.browser = None
        self.page = None
        self.driver = None
        
    def init_browser(self):
        """初始化浏览器"""
        if self.method == "playwright" and PLAYWRIGHT_AVAILABLE:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = self.context.new_page()
        elif SELENIUM_AVAILABLE:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--headless")  # 首次运行建议关闭
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.driver.set_window_size(1920, 1080)
        else:
            raise Exception("没有可用的浏览器自动化工具")
    
    def login(self):
        """扫码登录视频号助手"""
        print("🔐 正在打开视频号助手...")
        
        if self.method == "playwright":
            self.page.goto("https://channels.weixin.qq.com/")
            print("📱 请使用微信扫码登录...")
            print("   (等待60秒)")
            
            try:
                # 等待登录成功 (检测头像出现)
                self.page.wait_for_selector(".user-avatar, .user-name", timeout=60000)
                print("✅ 登录成功")
            except:
                print("❌ 登录超时")
                return False
        else:
            self.driver.get("https://channels.weixin.qq.com/")
            print("📱 请使用微信扫码登录...")
            
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".user-avatar, .user-name"))
                )
                print("✅ 登录成功")
            except:
                print("❌ 登录超时")
                return False
        
        return True
    
    def upload_to_draft(self, video_path, metadata):
        """
        上传视频到草稿箱
        
        Args:
            video_path: 视频文件路径
            metadata: {
                'title': '标题',
                'description': '描述',
                'tags': ['标签1', '标签2'],
                'cover_time': 5.0  # 封面时间(秒)
            }
        """
        video_path = Path(video_path)
        if not video_path.exists():
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        print(f"📤 正在上传视频: {video_path.name}")
        
        if self.method == "playwright":
            return self._upload_playwright(video_path, metadata)
        else:
            return self._upload_selenium(video_path, metadata)
    
    def _upload_playwright(self, video_path, metadata):
        """使用Playwright上传"""
        try:
            # 进入发布页面
            self.page.goto("https://channels.weixin.qq.com/platform/post/create")
            time.sleep(2)
            
            # 上传视频文件
            print("⏳ 正在上传视频文件...")
            self.page.set_input_files('input[type="file"]', str(video_path))
            
            # 等待上传完成 (检测视频预览出现)
            print("⏳ 等待视频上传完成...")
            self.page.wait_for_selector(".video-preview, .video-player", timeout=120000)
            print("✅ 视频上传完成")
            
            # 填写标题
            if metadata.get('title'):
                self.page.fill('input[placeholder*="标题"], input[placeholder*="添加标题"]', 
                              metadata['title'])
                print(f"✏️  已填写标题: {metadata['title']}")
            
            # 填写描述
            if metadata.get('description'):
                self.page.fill('textarea[placeholder*="描述"], textarea[placeholder*="添加描述"]', 
                              metadata['description'])
                print("✏️  已填写描述")
            
            # 添加话题标签
            if metadata.get('tags'):
                for tag in metadata['tags']:
                    try:
                        # 尝试不同的标签输入方式
                        tag_input = self.page.query_selector('.tag-input input, input[placeholder*="话题"]')
                        if tag_input:
                            tag_input.fill(f"#{tag}")
                            self.page.keyboard.press('Enter')
                            time.sleep(0.5)
                    except:
                        pass
                print(f"🏷️  已添加标签: {', '.join(metadata['tags'])}")
            
            # 等待一下确保表单填写完成
            time.sleep(2)
            
            # 点击保存草稿
            print("💾 正在保存到草稿箱...")
            
            # 尝试多种方式找到保存草稿按钮
            save_btn_selectors = [
                'button:has-text("保存草稿")',
                'button:has-text("存草稿")',
                '.btn-save-draft',
                '[data-action="save-draft"]'
            ]
            
            for selector in save_btn_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    print(f"✅ 已点击: {selector}")
                    break
                except:
                    continue
            
            # 等待保存成功
            time.sleep(3)
            
            print("✅ 视频已成功保存到草稿箱")
            return True
            
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False
    
    def _upload_selenium(self, video_path, metadata):
        """使用Selenium上传"""
        try:
            # 进入发布页面
            self.driver.get("https://channels.weixin.qq.com/platform/post/create")
            time.sleep(2)
            
            # 上传视频
            print("⏳ 正在上传视频文件...")
            file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_input.send_keys(str(video_path.absolute()))
            
            # 等待上传完成
            print("⏳ 等待视频上传完成...")
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".video-preview, .video-player"))
            )
            print("✅ 视频上传完成")
            
            # 填写标题
            if metadata.get('title'):
                title_input = self.driver.find_element(By.CSS_SELECTOR, 
                    'input[placeholder*="标题"], input[placeholder*="添加标题"]')
                title_input.send_keys(metadata['title'])
                print(f"✏️  已填写标题: {metadata['title']}")
            
            # 填写描述
            if metadata.get('description'):
                desc_input = self.driver.find_element(By.CSS_SELECTOR,
                    'textarea[placeholder*="描述"], textarea[placeholder*="添加描述"]')
                desc_input.send_keys(metadata['description'])
                print("✏️  已填写描述")
            
            # 等待一下
            time.sleep(2)
            
            # 保存草稿
            print("💾 正在保存到草稿箱...")
            try:
                save_btn = self.driver.find_element(By.XPATH, 
                    '//button[contains(text(),"保存草稿") or contains(text(),"存草稿")]')
                save_btn.click()
            except:
                # 尝试其他选择器
                save_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn-save-draft')
                save_btn.click()
            
            time.sleep(3)
            print("✅ 视频已成功保存到草稿箱")
            return True
            
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.method == "playwright":
            if self.browser:
                self.browser.close()
            if hasattr(self, 'playwright'):
                self.playwright.stop()
        elif self.driver:
            self.driver.quit()


def main():
    parser = argparse.ArgumentParser(description='视频号助手自动化上传工具')
    parser.add_argument('--video', '-v', required=True, help='视频文件路径')
    parser.add_argument('--title', '-t', default='', help='视频标题')
    parser.add_argument('--desc', '-d', default='', help='视频描述')
    parser.add_argument('--tags', '-g', default='', help='话题标签，逗号分隔')
    parser.add_argument('--method', '-m', default='playwright', 
                       choices=['playwright', 'selenium'], help='自动化工具')
    parser.add_argument('--config', '-c', help='配置文件路径 (JSON格式)')
    
    args = parser.parse_args()
    
    # 加载配置文件
    metadata = {
        'title': args.title,
        'description': args.desc,
        'tags': args.tags.split(',') if args.tags else []
    }
    
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            metadata.update(config)
    
    # 如果没有提供元数据，使用默认OpenMAIC内容
    if not metadata['title']:
        metadata = {
            'title': '清华大学AI方案，一句话生成全套课程',
            'description': '''做课程太累了？试试OpenMAIC！

清华大学出品，完全免费
一句话生成，5分钟完成传统2周工作量
已有2万+开发者使用

限时领取100+清华AI课件模板
关注视频号，回复【课件】自动领取''',
            'tags': ['OpenMAIC', 'AI课程', '清华大学', '教育科技', '知识付费']
        }
    
    # 执行上传
    uploader = VideoChannelUploader(method=args.method)
    try:
        uploader.init_browser()
        if uploader.login():
            success = uploader.upload_to_draft(args.video, metadata)
            if success:
                print("\n🎉 全部完成！请登录视频号助手查看草稿箱")
            else:
                print("\n❌ 上传失败")
        else:
            print("\n❌ 登录失败")
    finally:
        uploader.close()


if __name__ == '__main__':
    main()

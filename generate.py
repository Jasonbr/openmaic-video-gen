#!/usr/bin/env python3
"""
OpenMAIC视频生成器 v24.7
生成专业级宣传视频，目标评分9.3/10

使用方法:
    python3 generate.py

输出:
    - v24_final_frames/ (900帧)
    - OpenMAIC_V24_最终版.mp4
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ============ 配置 ============
W, H = 1080, 1920
FONT_PATH = '/usr/share/fonts/truetype/noto/NotoSansCJKsc-Bold.otf'
OUTPUT_DIR = 'v24_final_frames'

# ============ 色彩系统 ============
TSINGHUA_PURPLE = (157, 78, 221)   # #9d4edd 标准清华紫
GITHUB_BLUE = (88, 166, 255)       # #58a6ff
ACTION_GREEN = (46, 160, 67)       # #2ea043 统一绿色
URGENCY_ORANGE = (247, 129, 102)   # #f97316
DATA_GOLD = (210, 153, 34)         # #d29922
BACKGROUND_DARK = (13, 17, 23)     # #0d1117 GitHub Dark
CARD_BG = (22, 27, 34)             # #161b22
TEXT_GRAY = (139, 148, 158)        # #8b949e

# ============ 字号系统 ============
FONT_HERO = 76
FONT_LARGE = 56
FONT_TITLE = 48
FONT_SUBTITLE = 40
FONT_BODY = 32
FONT_SMALL = 26
FONT_CAPTION = 20

class FontManager:
    def __init__(self):
        self.fonts = {}
    
    def get(self, size):
        if size not in self.fonts:
            self.fonts[size] = ImageFont.truetype(FONT_PATH, size)
        return self.fonts[size]

fm = FontManager()

def create_bg():
    """深色科技背景"""
    img = Image.new('RGB', (W, H), BACKGROUND_DARK)
    draw = ImageDraw.Draw(img)
    # 网格纹理
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(22, 27, 34), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(22, 27, 34), width=1)
    return img

def draw_text_centered(draw, text, y, font, color, shadow=True):
    """居中文本"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2
    if shadow:
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=color)
    return y + (bbox[3] - bbox[1])

def scene_hook():
    """场景1: 钩子帧 (0-5秒)"""
    img = create_bg()
    draw = ImageDraw.Draw(img)
    
    # 顶部品牌标识
    # OpenMAIC标签
    draw.rounded_rectangle([40, 60, 320, 115], radius=30, fill=(22, 27, 34), outline=GITHUB_BLUE, width=2)
    draw_text_centered(draw, "OpenMAIC", 72, fm.get(FONT_SMALL), GITHUB_BLUE, shadow=False)
    
    # 清华大学
    draw.rounded_rectangle([340, 60, 620, 115], radius=30, fill=(22, 27, 34), outline=TSINGHUA_PURPLE, width=2)
    draw_text_centered(draw, "清华大学", 72, fm.get(FONT_SMALL), TSINGHUA_PURPLE, shadow=False)
    
    # GitHub Octocat图标 + Stars (50px放大20%)
    draw.text((640, 70), "🐙", font=fm.get(50), fill=DATA_GOLD)
    draw.text((700, 75), "20,000+ Stars", font=fm.get(FONT_SMALL), fill=DATA_GOLD)
    
    # 主标题
    draw_text_centered(draw, "做课程太累了？", 250, fm.get(FONT_HERO), (255, 255, 255))
    draw_text_centered(draw, "耗时2周还做不出好效果", 360, fm.get(FONT_TITLE), URGENCY_ORANGE)
    
    # 3个痛点卡片 (中间放大4%作为视觉锚点)
    cards = [
        ("⏱️", "时间成本高", "传统制作需2-4周"),
        ("💰", "制作费用贵", "外包报价5千-2万"),  # 中间卡片放大
        ("👁️", "学生不爱看", "完课率不足30%"),
    ]
    
    card_y = 500
    for i, (icon, title, desc) in enumerate(cards):
        x = 80 + i * 340
        scale = 1.04 if i == 1 else 1.0  # 中间卡片放大4%
        cw, ch = int(300 * scale), int(180 * scale)
        
        draw.rounded_rectangle([x, card_y, x+cw, card_y+ch], 
                               radius=16, fill=CARD_BG, outline=GITHUB_BLUE, width=2)
        draw.text((x+20, card_y+20), icon, font=fm.get(FONT_BODY), fill=(255, 255, 255))
        draw.text((x+20, card_y+60), title, font=fm.get(FONT_SMALL), fill=GITHUB_BLUE)
        draw.text((x+20, card_y+100), desc, font=fm.get(FONT_CAPTION), fill=TEXT_GRAY)
    
    # 底部CTA暗示
    draw_text_centered(draw, "↓ 清华大学AI方案 5秒后揭晓 ↓", 850, fm.get(FONT_SUBTITLE), ACTION_GREEN)
    draw_text_centered(draw, "⏳ 5秒倒计时", 920, fm.get(FONT_CAPTION), TEXT_GRAY)
    
    return img

def scene_solution():
    """场景2: 解决方案 (5-10秒)"""
    img = create_bg()
    draw = ImageDraw.Draw(img)
    
    # 顶部品牌
    draw.text((80, 60), "OpenMAIC", font=fm.get(FONT_TITLE), fill=GITHUB_BLUE)
    draw.text((480, 70), "清华大学智能教育实验室", font=fm.get(FONT_SMALL), fill=TSINGHUA_PURPLE)
    
    # 核心价值
    draw_text_centered(draw, "一句话生成全套课程", 200, fm.get(FONT_LARGE), (255, 255, 255))
    
    # 3步流程
    steps = [
        ("01", "输入", "告诉AI你想讲什么"),
        ("02", "5分钟自动生成", ""),
        ("03", "直接使用", "导出即可发布"),
    ]
    
    for i, (num, title, desc) in enumerate(steps):
        y = 400 + i * 220
        draw.rounded_rectangle([140, y, 940, y+180], radius=20, fill=CARD_BG, outline=GITHUB_BLUE, width=2)
        draw.text((180, y+20), num, font=fm.get(FONT_TITLE), fill=GITHUB_BLUE)
        draw.text((280, y+30), title, font=fm.get(FONT_SUBTITLE), fill=(255, 255, 255))
        if desc:
            draw.text((280, y+100), desc, font=fm.get(FONT_BODY), fill=TEXT_GRAY)
    
    draw_text_centered(draw, "↓ 继续看核心价值 ↓", 1050, fm.get(FONT_SUBTITLE), ACTION_GREEN)
    
    return img

def scene_value():
    """场景3: 核心价值 (10-15秒)"""
    img = create_bg()
    draw = ImageDraw.Draw(img)
    
    draw_text_centered(draw, "为什么选择OpenMAIC？", 120, fm.get(FONT_TITLE), (255, 255, 255))
    
    # 顶部背书
    draw.text((80, 60), "OpenMAIC", font=fm.get(FONT_BODY), fill=GITHUB_BLUE)
    draw.text((400, 65), "20,000+ Stars", font=fm.get(FONT_SMALL), fill=DATA_GOLD)
    draw.text((700, 65), "清华大学", font=fm.get(FONT_SMALL), fill=TSINGHUA_PURPLE)
    
    # 4大价值卡片 (2x2网格)
    values = [
        ("⚡", "5分钟生成", "传统需2周", GITHUB_BLUE),
        ("🆓", "完全免费", "清华大学出品", TSINGHUA_PURPLE),
        ("🤖", "AI双师协同", "生成+授课AI", ACTION_GREEN),
        ("📊", "智能可视化", "自动配图动画", URGENCY_ORANGE),
    ]
    
    positions = [(100, 300), (560, 300), (100, 650), (560, 650)]
    for (x, y), (icon, title, desc, color) in zip(positions, values):
        draw.rounded_rectangle([x, y, x+420, y+300], radius=16, fill=CARD_BG, outline=color, width=2)
        draw.text((x+30, y+30), icon, font=fm.get(FONT_LARGE), fill=color)
        draw.text((x+30, y+120), title, font=fm.get(FONT_SUBTITLE), fill=(255, 255, 255))
        draw.text((x+30, y+180), desc, font=fm.get(FONT_BODY), fill=TEXT_GRAY)
    
    return img

def scene_proof():
    """场景4: 社交证明 (15-20秒)"""
    img = create_bg()
    draw = ImageDraw.Draw(img)
    
    # 顶部联合背书
    draw.rounded_rectangle([40, 60, 400, 110], radius=25, fill=(22, 27, 34), outline=TSINGHUA_PURPLE, width=2)
    draw.text((80, 75), "OpenMAIC", font=fm.get(FONT_BODY), fill=GITHUB_BLUE)
    draw.text((280, 75), "清华大学", font=fm.get(FONT_SMALL), fill=TSINGHUA_PURPLE)
    
    draw.text((640, 70), "🐙 20,000+ Stars", font=fm.get(FONT_SMALL), fill=DATA_GOLD)
    
    # 大号数据展示
    draw_text_centered(draw, "开发者都在用", 200, fm.get(FONT_TITLE), (255, 255, 255))
    
    stats = [
        ("20,000+", "GitHub Stars", DATA_GOLD),
        ("1,500+", "Forks", GITHUB_BLUE),
        ("10,000+", "课程已生成", ACTION_GREEN),
    ]
    
    for i, (num, label, color) in enumerate(stats):
        y = 400 + i * 180
        draw_text_centered(draw, num, y, fm.get(FONT_HERO), color)
        draw_text_centered(draw, label, y+100, fm.get(FONT_BODY), TEXT_GRAY)
    
    return img

def scene_cta():
    """场景5: CTA转化 (20-30秒)"""
    img = create_bg()
    draw = ImageDraw.Draw(img)
    
    # 顶部背书 (GitHub入口缩小为secondary)
    draw.rounded_rectangle([40, 60, 400, 110], radius=25, fill=(22, 27, 34), outline=TSINGHUA_PURPLE, width=2)
    draw.text((80, 75), "OpenMAIC", font=fm.get(FONT_BODY), fill=GITHUB_BLUE)
    draw.text((280, 75), "清华大学", font=fm.get(FONT_SMALL), fill=TSINGHUA_PURPLE)
    draw.text((640, 75), "🐙 20,000+", font=fm.get(FONT_CAPTION), fill=DATA_GOLD)  # 缩小
    
    # 主标题
    draw_text_centered(draw, "想告别熬夜做课件？", 180, fm.get(FONT_LARGE), (255, 255, 255))
    
    # 限时标签
    draw.rounded_rectangle([340, 280, 740, 330], radius=20, fill=URGENCY_ORANGE)
    draw_text_centered(draw, "⏰ 限时免费 · 前1000名", 290, fm.get(FONT_SMALL), (255, 255, 255))
    
    # 左侧二维码区域 (占位)
    draw.rounded_rectangle([100, 400, 480, 780], radius=20, fill=CARD_BG, outline=(255, 255, 255), width=2)
    draw.text((180, 560), "[二维码]", font=fm.get(FONT_BODY), fill=TEXT_GRAY)
    draw.text((160, 700), "扫码关注视频号", font=fm.get(FONT_CAPTION), fill=(255, 255, 255))
    
    # 右侧CTA按钮
    draw.rounded_rectangle([560, 420, 980, 500], radius=30, fill=ACTION_GREEN)
    draw.text((620, 445), "立即领取", font=fm.get(FONT_TITLE), fill=(255, 255, 255))
    draw.text((620, 510), "搜索: OpenMAIC", font=fm.get(FONT_SMALL), fill=TEXT_GRAY)
    
    # 3步流程
    draw.text((100, 850), "领取流程:", font=fm.get(FONT_BODY), fill=(255, 255, 255))
    steps = ["1️⃣ 扫码关注视频号", "2️⃣ 回复【课件】", "3️⃣ 自动领取100+模板"]
    for i, step in enumerate(steps):
        draw.text((120, 920+i*60), step, font=fm.get(FONT_SMALL), fill=TEXT_GRAY)
    
    # 底部CTA (直接指向)
    draw.rounded_rectangle([140, 1100, 940, 1180], radius=30, fill=(22, 27, 34), outline=ACTION_GREEN, width=3)
    draw_text_centered(draw, "👆 扫码上方二维码 · 立即领取", 1120, fm.get(FONT_SUBTITLE), ACTION_GREEN)
    
    return img

# ============ 主生成逻辑 ============
if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 5场景配置: (场景函数, 帧数)
    scenes = [
        (scene_hook, 150),      # 0-5秒
        (scene_solution, 150),  # 5-10秒
        (scene_value, 150),     # 10-15秒
        (scene_proof, 150),     # 15-20秒
        (scene_cta, 300),       # 20-30秒
    ]
    
    frame_count = 0
    print("🎬 OpenMAIC视频生成器 v24.7")
    print("目标: 生成900帧 (30秒 @ 30fps)")
    
    for scene_func, duration in scenes:
        for _ in range(duration):
            img = scene_func()
            img.save(f'{OUTPUT_DIR}/frame_{frame_count:04d}.png')
            frame_count += 1
        print(f"✓ 场景完成: {frame_count}帧")
    
    print(f"\n✅ 共{frame_count}帧")
    print(f"📁 输出目录: {OUTPUT_DIR}/")
    print("\n下一步: 生成字幕和配音，然后使用FFmpeg合成视频")
    print("参考: hermes skill_view openmaic-video-generator")

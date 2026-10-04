import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def create_styled_qr(url, output_path, title_text="亮亮精靈護眼大冒險", subtitle_text="請用手機/平板掃描 QR Code 進入", logo_path=None):
    # 1. Create QR Code with high error correction (Level H = 30%)
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Emerald dark color (#047857) on white
    img_qr = qr.make_image(fill_color="#047857", back_color="#FFFFFF").convert("RGB")
    width, height = img_qr.size

    # 2. Add Center Logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            # Logo size ~ 20% of QR width
            logo_size = int(width * 0.22)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Create a rounded white background circle/card for logo
            bg_logo = Image.new("RGBA", (logo_size + 12, logo_size + 12), (255, 255, 255, 255))
            draw_bg = ImageDraw.Draw(bg_logo)
            draw_bg.ellipse([0, 0, logo_size + 11, logo_size + 11], fill="#FFFFFF", outline="#10B981", width=3)
            
            # Mask logo into circle
            mask = Image.new("L", (logo_size, logo_size), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, logo_size, logo_size), fill=255)
            
            bg_logo.paste(logo, (6, 6), mask)

            # Paste logo into center of QR code
            logo_x = (width - bg_logo.width) // 2
            logo_y = (height - bg_logo.height) // 2
            img_qr.paste(bg_logo, (logo_x, logo_y), bg_logo)
        except Exception as e:
            print(f"Logo embedding note: {e}")

    # 3. Canvas setup with top header and bottom footer
    header_h = 100
    footer_h = 75
    padding_x = 40
    
    total_w = width + (padding_x * 2)
    total_h = height + header_h + footer_h

    canvas = Image.new("RGB", (total_w, total_h), "#0F172A")
    draw = ImageDraw.Draw(canvas)

    # Rounded card frame
    card_margin = 10
    draw.rounded_rectangle(
        [card_margin, card_margin, total_w - card_margin, total_h - card_margin],
        radius=24,
        fill="#1E293B",
        outline="#10B981",
        width=4
    )

    # Paste QR code
    canvas.paste(img_qr, (padding_x, header_h))

    # Traditional Chinese Font
    font_path = "c:/windows/fonts/msjh.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 24, index=0)
        sub_font = ImageFont.truetype(font_path, 15, index=0)
        url_font = ImageFont.truetype(font_path, 14, index=0)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        url_font = ImageFont.load_default()

    # Draw Header & Footer text
    draw.text((total_w / 2, 40), title_text, font=title_font, fill="#FFD000", anchor="mm")
    draw.text((total_w / 2, 75), subtitle_text, font=sub_font, fill="#94A3B8", anchor="mm")
    draw.text((total_w / 2, total_h - 40), f"連線網址：{url}", font=url_font, fill="#38BDF8", anchor="mm")

    canvas.save(output_path, quality=95)
    print(f"[OK] QR Code saved to: {output_path}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="產生亮亮精靈護眼大冒險 QR Code (支援 LAN 區網與 GitHub Pages 雲端網址)")
    parser.add_argument("--url", "--cloud-url", type=str, default="https://your-school-url.github.io/eye-adventure/", help="GitHub Pages 或雲端部署網址 (例如: https://<username>.github.io/eye-adventure/)")
    parser.add_argument("--port", type=int, default=8080, help="區域網路服務埠號 (預設: 8080)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(base_dir, "assets")
    logo_path = os.path.join(assets_dir, "liang_liang.jpg")

    os.makedirs(assets_dir, exist_ok=True)

    local_ip = get_local_ip()
    lan_url = f"http://{local_ip}:{args.port}/index.html"
    cloud_url = args.url

    print(f"Local LAN IP detected: {local_ip}")
    print(f"Classroom LAN URL: {lan_url}")
    print(f"Cloud/GitHub Pages URL: {cloud_url}")

    # Generate LAN QR Code with Logo
    out_lan = os.path.join(assets_dir, "lan_qr_code.png")
    create_styled_qr(lan_url, out_lan, "亮亮精靈護眼大冒險 (課堂區網版)", "同班同學連結同一 Wi-Fi 即可掃碼進場", logo_path)

    # Generate Cloud QR Code
    out_cloud = os.path.join(assets_dir, "cloud_qr_code.png")
    create_styled_qr(cloud_url, out_cloud, "亮亮精靈護眼大冒險 (雲端正式版)", "掃描開啟網際網路線上互動平台", logo_path)

    # Save standard project QR (uses cloud_url if custom URL is provided, otherwise lan_url)
    out_proj = os.path.join(assets_dir, "eye_adventure_qr.png")
    target_url = cloud_url if cloud_url != "https://your-school-url.github.io/eye-adventure/" else lan_url
    create_styled_qr(target_url, out_proj, "亮亮精靈護眼大冒險", "手機/平板掃描 QR Code 立即體驗", logo_path=logo_path)

    # Also update artifact dir if specified or environment present
    artifact_dir = os.environ.get("ANTIGRAVITY_ARTIFACT_DIR")
    if artifact_dir and os.path.exists(artifact_dir):
        create_styled_qr(lan_url, os.path.join(artifact_dir, "lan_qr_code.png"), "亮亮精靈護眼大冒險 (課堂區網版)", "同班同學連結同一 Wi-Fi 即可掃碼進場", logo_path)
        create_styled_qr(cloud_url, os.path.join(artifact_dir, "cloud_qr_code.png"), "亮亮精靈護眼大冒險 (雲端正式版)", "掃描開啟網際網路線上互動平台", logo_path)
        create_styled_qr(target_url, os.path.join(artifact_dir, "eye_adventure_qr.png"), "亮亮精靈護眼大冒險", "手機/平板掃描 QR Code 立即體驗", logo_path=logo_path)

if __name__ == "__main__":
    main()

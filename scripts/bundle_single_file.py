import base64
import os
import re

base_dir = r"h:\電腦桌面20260817\ANTI\教材編輯"
index_path = os.path.join(base_dir, "index.html")
out_path = os.path.join(base_dir, "single_file_eye_adventure.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace asset image URLs with Base64 data URLs
assets_map = {
    "assets/liang_liang.jpg": os.path.join(base_dir, "assets", "liang_liang.jpg"),
    "assets/fog_monster.jpg": os.path.join(base_dir, "assets", "fog_monster.jpg"),
    "assets/green_tree.jpg": os.path.join(base_dir, "assets", "green_tree.jpg"),
    "assets/park_kite.jpg": os.path.join(base_dir, "assets", "park_kite.jpg"),
}

for rel_path, abs_path in assets_map.items():
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode("utf-8")
            data_url = f"data:image/jpeg;base64,{b64_str}"
            content = content.replace(rel_path, data_url)

with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully generated portable single-file bundle: {out_path}")

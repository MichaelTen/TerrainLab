import os
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

# === CONFIG ===
target_scale = 88 / 64
input_folder = "."
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(".png")])
total = len(files)

print(f"Found {total} PNG files.\n")

def upscale_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.load()

        # Keep original mode if possible (avoid unnecessary conversion)
        original_mode = img.mode

        # Step 1: upscale 2x with NEAREST (perfect pixel scaling)
        img_2x = img.resize((img.width * 2, img.height * 2), Image.NEAREST)

        # Step 2: resize down to exact target with LANCZOS
        new_width = int(round(img.width * target_scale))
        new_height = int(round(img.height * target_scale))

        final = img_2x.resize((new_width, new_height), Image.LANCZOS)

        final.save(output_path, format="PNG")

for i, filename in enumerate(files, start=1):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    try:
        upscale_image(input_path, output_path)
        print(f"{i} / {total}  →  {filename}")
    except Exception as e:
        print(f"{i} / {total}  →  FAILED: {filename}")
        print(f"    Reason: {e}")

print("\nDone.")

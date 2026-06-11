from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ChatGPT Image Jun 11, 2026, 10_28_20 PM.png"
ASSETS = ROOT / "frontend" / "src" / "assets"
PUBLIC = ROOT / "frontend" / "public"


def clean_mask(mask, min_component_area=800):
    width, height = mask.size
    pixels = mask.load()
    seen = set()
    keep = set()

    for y in range(height):
        for x in range(width):
            if (x, y) in seen or pixels[x, y] == 0:
                continue

            stack = [(x, y)]
            component = []
            seen.add((x, y))

            while stack:
                cx, cy = stack.pop()
                component.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue
                    if (nx, ny) in seen or pixels[nx, ny] == 0:
                        continue
                    seen.add((nx, ny))
                    stack.append((nx, ny))

            if len(component) >= min_component_area:
                keep.update(component)

    cleaned = Image.new("L", mask.size, 0)
    cleaned_pixels = cleaned.load()
    for x, y in keep:
        cleaned_pixels[x, y] = 255
    return cleaned


def recolor(source, mask, amber=(242, 197, 66), green=(61, 201, 154)):
    source = source.convert("RGBA")
    width, height = source.size
    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    input_pixels = source.load()
    output_pixels = output.load()
    mask_pixels = mask.load()

    for y in range(height):
        for x in range(width):
            r, g, b, a = input_pixels[x, y]
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if mask_pixels[x, y] and luminance < 140 and a > 0:
                alpha = int(max(0, min(255, (118 - luminance) / 118 * 255)))
                mix = x / max(1, width - 1)
                color = tuple(int(amber[i] * (1 - mix) + green[i] * mix) for i in range(3))
                output_pixels[x, y] = (*color, alpha)

    return output.filter(ImageFilter.UnsharpMask(radius=1, percent=130, threshold=3))


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)

    image = Image.open(SOURCE).convert("RGBA")
    width, height = image.size
    pixels = image.load()
    threshold = 82
    coords = []

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < threshold and a > 0:
                coords.append((x, y))

    if not coords:
        raise RuntimeError("No logo pixels detected")

    xs = [coord[0] for coord in coords]
    ys = [coord[1] for coord in coords]
    margin = 28
    left = max(0, min(xs) - margin)
    top = max(0, min(ys) - margin)
    right = min(width, max(xs) + margin)
    bottom = min(height, max(ys) + margin)

    crop = image.crop((left, top, right, bottom))
    mask = Image.new("L", crop.size, 0)
    mask_pixels = mask.load()
    crop_pixels = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, a = crop_pixels[x, y]
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < threshold and a > 0:
                mask_pixels[x, y] = 255
    mask = clean_mask(mask)

    wordmark = recolor(crop, mask)
    wordmark.save(ASSETS / "skaut-logo.png")

    wordmark_width, wordmark_height = wordmark.size
    icon_crop = wordmark.crop((0, 0, min(wordmark_width, int(wordmark_height * 1.25)), wordmark_height))
    icon_bounds = icon_crop.getbbox()
    if icon_bounds:
        icon_crop = icon_crop.crop(icon_bounds)

    square_size = max(icon_crop.size) + 40
    icon = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
    icon.alpha_composite(
        icon_crop,
        ((square_size - icon_crop.width) // 2, (square_size - icon_crop.height) // 2),
    )
    icon = icon.resize((512, 512), Image.Resampling.LANCZOS)
    icon.save(ASSETS / "skaut-icon.png")
    icon.resize((192, 192), Image.Resampling.LANCZOS).save(PUBLIC / "skaut-icon.png")

    print(f"source={image.size} crop={(left, top, right, bottom)} wordmark={wordmark.size}")


if __name__ == "__main__":
    main()

"""Generate a Markdown-style app icon (.ico) for MD Reader.

Draws a rounded-square badge containing the classic Markdown mark
(an 'M' next to a downward arrow). Rendered at 4x then downscaled for
smooth anti-aliased edges, and saved as a multi-resolution .ico plus a
preview .png.
"""

from PIL import Image, ImageDraw

SCALE = 4
S = 256 * SCALE  # working canvas size

BADGE = (76, 110, 245, 255)     # indigo
BADGE_EDGE = (60, 88, 210, 255)  # slightly darker border
GLYPH = (255, 255, 255, 255)    # white


def px(v):
    return int(v * SCALE)


def make():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Rounded badge
    pad = px(14)
    radius = px(46)
    d.rounded_rectangle([pad, pad, S - pad, S - pad], radius=radius,
                        fill=BADGE, outline=BADGE_EDGE, width=px(3))

    # --- "M" as a rounded polyline ---
    m_pts = [
        (px(50), px(176)),
        (px(50), px(84)),
        (px(100), px(134)),
        (px(150), px(84)),
        (px(150), px(176)),
    ]
    d.line(m_pts, fill=GLYPH, width=px(22), joint="curve")
    # round the end caps
    for (x, y) in [m_pts[0], m_pts[-1]]:
        r = px(11)
        d.ellipse([x - r, y - r, x + r, y + r], fill=GLYPH)

    # --- downward arrow ---
    cx = px(182)
    stem_w = px(22)
    d.rectangle([cx - stem_w // 2, px(84), cx + stem_w // 2, px(140)], fill=GLYPH)
    d.polygon([(px(158), px(132)), (px(206), px(132)), (cx, px(178))], fill=GLYPH)

    # downscale for anti-aliasing
    return img.resize((256, 256), Image.LANCZOS)


def main():
    icon = make()
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon.save("icon.ico", format="ICO", sizes=sizes)
    icon.save("icon_preview.png", format="PNG")
    print("Wrote icon.ico and icon_preview.png")


if __name__ == "__main__":
    main()

"""DIG Career Thrust visual theme for videos, teasers and thumbnails (Naveen, 23 Nov 2026).

Matches the website https://web.digcareerthrust.com (dct-platform theme.css / site.css):
indigo -> violet hero gradient (#312E81 -> #4F46E5 -> #7C3AED) with soft coral and cyan glows,
white rounded cards with dark-ink text, coral accent, mint for "good" facts, Manrope font.
"""
from PIL import Image, ImageDraw, ImageFilter

PRIMARY = (79, 70, 229)       # #4F46E5  --dct-primary
PRIMARY_DARK = (67, 56, 202)  # #4338CA  --dct-primary-dark
VIOLET = (124, 58, 237)       # #7C3AED  --dct-violet
NAVY = (49, 46, 129)          # #312E81  hero gradient start
CORAL = (242, 98, 107)        # #F2626B  --dct-accent
MINT = (16, 185, 129)         # #10B981  --dct-mint
CYAN = (34, 211, 238)         # #22D3EE  hero glow
AMBER = (251, 191, 36)        # #FBBF24  highlight
INK = (30, 34, 53)            # #1E2235  --dct-ink
MUTED = (102, 112, 133)       # #667085  --dct-muted
SOFT = (224, 231, 255)        # #E0E7FF  light text on the gradient
PRIMARY_SOFT = (238, 240, 255)  # #EEF0FF
WHITE = (255, 255, 255)
FONT = "Manrope"              # files assets/Manrope-{Medium,SemiBold,Bold,ExtraBold}.ttf
CHANNEL = "DIG Career Thrust"
HANDLE = "@digcareerthrust"
TAGLINE = "Daily Govt Job Updates"


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_bg(W, H, glows=True):
    """135-degree indigo -> violet gradient like the website hero, with blurred coral/cyan glows. RGBA."""
    small = Image.new("RGB", (max(2, W // 8), max(2, H // 8)))
    sw, shh = small.size
    px = small.load()
    for y in range(shh):
        for x in range(sw):
            t = (x / sw + y / shh) / 2          # 0 top-left .. 1 bottom-right
            c = _lerp(NAVY, PRIMARY, t / 0.45) if t < 0.45 else _lerp(PRIMARY, VIOLET, (t - 0.45) / 0.55)
            px[x, y] = c
    im = small.resize((W, H), Image.BICUBIC).convert("RGBA")
    if glows:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        r1 = int(min(W, H) * 0.42); r2 = int(min(W, H) * 0.36)
        d.ellipse([W - r1 * 1.3, -r1 * 0.9, W + r1 * 0.7, r1 * 1.1], fill=CORAL + (120,))
        d.ellipse([-r2 * 0.6, H - r2 * 1.2, r2 * 1.4, H + r2 * 0.8], fill=CYAN + (85,))
        g = g.filter(ImageFilter.GaussianBlur(min(W, H) // 9))
        im.alpha_composite(g)
    return im


def header_band(W, h):
    """Translucent dark band behind the logo + channel name."""
    return Image.new("RGBA", (W, h), (20, 18, 60, 70))

#!/usr/bin/env python3
"""page_render_v1.py -- draw the screens a fleet program shows, as PNG files, from the PC harness.

ppl_run_v3e records every LINE_P, RECT_P, FILLPOLY_P, TEXTOUT_P ... with its arguments but never
renders a pixel, so a page can look right in the dump and wrong on the calculator: BurrLab beta 1o's
Family map was a solid dark gray box for ten days (a one-colour RECT_P fills, Lessons Learned s6) and
nobody saw it until Roger ran it on his G1 (7 Nov 2026).  This tool paints each captured screen with
PIL, following the calculator's own rules where the harness knows them:
  - RECT_P with ONE colour fills the rectangle with it (edge and fill); with two, edge and fill
  - FILLPOLY_P with an alpha blends; TRIANGLE_P fills; ARC_P draws a ring; PIXON_P one pixel
  - BLIT_P carries a grob's shapes to the target WITH their offset and the grob's DIMGROB_P
    background (ppl_run keeps the arguments unchanged; this subclass tracks the offset)
  - DRAWMENU paints the six soft keys at y 218-239
Text is drawn with DejaVu Sans at a size per HP font (an estimate: the Prime's glyphs differ), so
sizes and overlaps are approximate -- text_overlap_v1 and label_fit_v1 remain the measure for text.

usage:
    python3 page_render_v1.py PROGRAM.txt --call "Prog()" [--key K]... [--tap X,Y]...
        [--drag "x1,y1;x2,y2;..."]... [--choose N]... [--input "a=1"]... --out DIR [--last N]
Every captured screen becomes DIR/screen_NN.png (the last N only, with --last).  Same script
options as ppl_run_v3e, but --key, --tap and --drag are queued in the order they are given (ppl_run's
CLI queues every key before any tap); --drag queues a finger drag through the points, lifted at the
end.  CHOOSE and INPUT answers are taken in order as the dialogs open, as in ppl_run.

Python 3, PIL (Pillow).  Roger Metcalf / Claude, 7 Nov 2026.
"""
import sys, os, re, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ppl_run_v3e as R
from PIL import Image, ImageDraw, ImageFont

FONTS = {}
_FONT_PX = {0: 10, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18, 6: 20, 7: 22}


def font(n):
    n = int(n or 0)
    if n not in FONTS:
        px = _FONT_PX.get(n, 12)
        try:
            FONTS[n] = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', px - 1)
        except OSError:
            FONTS[n] = ImageFont.load_default()
    return FONTS[n]


def rgb(c, default=(0, 0, 0)):
    if c is None:
        return default
    try:
        v = int(c) & 0xFFFFFF
    except (TypeError, ValueError):
        return default
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255)


def nums(seq):
    out = []
    for v in seq:
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(float(v))
    return out


class Renderer(R.Harness):
    """ppl_run's harness with blit offsets and grob backgrounds carried into the screens."""

    def _blit(self, a):
        gi = [i for i, v in enumerate(a) if isinstance(v, R.Grob)]
        if not gi:
            raise R.Unsupported('BLIT_P without a graphic')
        if len(gi) == 1:
            trg, src, si = self.grobs['G0'], a[gi[0]], gi[0]
        else:
            trg, src, si = a[gi[0]], a[gi[1]], gi[1]
        offs = [v for v in a[(gi[0] + 1 if len(gi) > 1 else 0):si] if isinstance(v, float)]
        dx, dy = (offs + [0.0, 0.0])[:2]
        bg = R.Shape('BG', [dx, dy, float(src.w), float(src.h), float(src.bg)], trg.name)
        bg.dx = bg.dy = 0.0
        copied = [bg]
        for it in src.items:
            if isinstance(it, R.Text):
                t = R.Text(it.text, it.x + dx, it.y + dy, it.font, it.color, it.width, it.bg,
                           trg.name, it.func)
                copied.append(t)
            else:
                s = R.Shape(it.cmd, it.args, trg.name)
                s.dx = getattr(it, 'dx', 0.0) + dx
                s.dy = getattr(it, 'dy', 0.0) + dy
                copied.append(s)
        if dx == 0 and dy == 0 and src.w >= 320 and src.h >= 240:
            trg.items = copied                      # a whole-screen copy replaces the target
            trg.menu = None
        else:
            trg.items.extend(copied)
        self.log.append(('BLIT_P', a))
        self._draws += 1
        if trg.name == 'G0':
            self._capture('blit')
        return 0.0


def points_of(v):
    """FILLPOLY_P's points: {{x,y},...} or a flat {x1,y1,x2,y2,...}."""
    if isinstance(v, list):
        if v and isinstance(v[0], list):
            return [(float(p[0]), float(p[1])) for p in v]
        f = nums(v)
        return list(zip(f[0::2], f[1::2]))
    return []


def paint(screen, path):
    img = Image.new('RGBA', (320, 240), (255, 255, 255, 255))
    d = ImageDraw.Draw(img, 'RGBA')
    for it in screen.items:
        if isinstance(it, R.Text):
            d.text((it.x, it.y), it.text, fill=rgb(it.color), font=font(it.font))
            continue
        dx, dy = getattr(it, 'dx', 0.0), getattr(it, 'dy', 0.0)
        a = it.args
        if it.cmd == 'BG':
            x, y, w, h, c = a
            d.rectangle([x, y, x + w - 1, y + h - 1], fill=rgb(c, (255, 255, 255)))
        elif it.cmd in ('LINE_P', 'LINE'):
            f = nums(a)
            if len(f) >= 4:
                d.line([f[0] + dx, f[1] + dy, f[2] + dx, f[3] + dy],
                       fill=rgb(f[4] if len(f) > 4 else None), width=1)
        elif it.cmd in ('RECT_P', 'RECT'):
            f = nums(a)
            if len(f) >= 4:
                x1, y1, x2, y2 = min(f[0], f[2]) + dx, min(f[1], f[3]) + dy, max(f[0], f[2]) + dx, max(f[1], f[3]) + dy
                if len(f) == 4:
                    d.rectangle([x1, y1, x2, y2], outline=(0, 0, 0), fill=(0, 0, 0))
                elif len(f) == 5:                    # ONE colour: edge AND fill (the calculator)
                    d.rectangle([x1, y1, x2, y2], outline=rgb(f[4]), fill=rgb(f[4]))
                else:
                    d.rectangle([x1, y1, x2, y2], outline=rgb(f[4]), fill=rgb(f[5]))
        elif it.cmd in ('PIXON_P', 'PIXON'):
            f = nums(a)
            if len(f) >= 2:
                d.point([f[0] + dx, f[1] + dy], fill=rgb(f[2] if len(f) > 2 else None))
        elif it.cmd == 'FILLPOLY_P':
            pts = points_of(a[0]) if a else []
            rest = nums(a[1:])
            col = rgb(rest[0] if rest else None)
            alpha = int(rest[1]) if len(rest) > 1 else 255
            if len(pts) >= 3:
                d.polygon([(x + dx, y + dy) for x, y in pts], fill=col + (max(0, min(255, alpha)),))
        elif it.cmd == 'TRIANGLE_P':
            f = nums(a)
            if len(f) >= 6:
                d.polygon([(f[0] + dx, f[1] + dy), (f[2] + dx, f[3] + dy), (f[4] + dx, f[5] + dy)],
                          fill=rgb(f[6] if len(f) > 6 else None))
        elif it.cmd in ('ARC_P', 'ARC'):
            f = nums(a)
            if len(f) >= 3:
                x, y, r = f[0] + dx, f[1] + dy, f[2]
                d.ellipse([x - r, y - r, x + r, y + r], outline=rgb(f[3] if len(f) > 3 else None))
    if screen.menu:
        d.rectangle([0, 218, 319, 239], fill=(230, 230, 230), outline=(160, 160, 160))
        for i, lab in enumerate(screen.menu[:6]):
            x0 = int(i * 53.33)
            d.rectangle([x0, 218, x0 + 52, 239], outline=(160, 160, 160))
            d.text((x0 + 3, 223), str(lab), fill=(0, 0, 0), font=font(1))
    img.convert('RGB').save(path)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Paint the screens a PPL program shows, via ppl_run_v3e.')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--call', action='append', default=[])
    ap.add_argument('--choose', action='append', default=[])
    ap.add_argument('--input', action='append', default=[])
    ap.add_argument('--key', action='append', default=[])
    ap.add_argument('--tap', action='append', default=[])
    ap.add_argument('--drag', action='append', default=[])
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', required=True)
    ap.add_argument('--last', type=int, default=0)
    o = ap.parse_args(argv)
    os.makedirs(o.out, exist_ok=True)
    h = Renderer(seed=o.seed)
    h.max_screens = 400
    for f in o.files:
        h.load_path(f)
    for c in o.choose:
        h.choose(int(c) if re.fullmatch(r'-?\d+', c) else c)
    for s in o.input:
        h.answer(R._parse_input_spec(s))
    # keys, taps and drags are queued IN THE ORDER GIVEN on the command line (ppl_run_v3e's
    # CLI queues every --key before any --tap, so a tap can never come between two keys there)
    args = sys.argv[1:] if argv is None else list(argv)
    i = 0
    while i < len(args):
        if args[i] == '--key' and i + 1 < len(args):
            h.press(R._parse_key(args[i + 1])); i += 2
        elif args[i] == '--tap' and i + 1 < len(args):
            x, y = args[i + 1].split(',')
            h.tap(float(x), float(y)); i += 2
        elif args[i] == '--drag' and i + 1 < len(args):
            pts = [tuple(float(v) for v in p.split(',')) for p in args[i + 1].split(';') if p.strip()]
            h.drag(pts); i += 2
        else:
            i += 1
    rc = 0
    for expr in o.call:
        try:
            r = h.execute(expr)
            print('%s -> %s' % (expr, R.interp._format(r)))
        except (R.PPLError, R.Unsupported, R.HarnessStall, R.HarnessScriptError) as e:
            stack = ' > '.join(getattr(e, 'ppl_stack', []) or [])
            print('%s -> %s%s: %s' % (expr, type(e).__name__, (' in ' + stack) if stack else '', e))
            rc = 1
    screens = h.screens[-o.last:] if o.last else h.screens
    for s in screens:
        p = os.path.join(o.out, 'screen_%02d.png' % s.index)
        paint(s, p)
        print('%s  %s (%s, %d texts, %d shapes)' % (p, s.reason, s.func, len(s.texts), len(s.shapes)))
    for w in h.warnings:
        print('WARNING:', w)
    return rc


if __name__ == '__main__':
    sys.exit(main())

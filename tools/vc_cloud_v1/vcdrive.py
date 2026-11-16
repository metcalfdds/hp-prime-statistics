# -*- coding: utf-8 -*-
"""vcdrive.py -- drive the HP Prime Virtual Calculator on the Xvfb display with xdotool (the cloud workspace, Wine).
Round 16, 15 Nov 2026; tools/vc_cloud_v1/README.md says how the calculator is set up there.

WHAT IT GIVES A TOUR SCRIPT
    key('Enter'), soft(3), tap(x, y)     one press on the skin, a soft key (1-6), or the calculator's own screen
    act(key, 'Right')                    the press, then wait until the screen has changed and stopped changing;
                                         a press that changed nothing is sent again (see below), False if it never did
    pick(6)                              item 6 of an open CHOOSE box (its digit; Downs and Enter above 9)
    catalog(); run_program('AnovaLab')   Shift, 1; then the highlight to that row by the arrow keys, and Run
    cap(path, x3=False); ocr(path, crop) a 320 x 240 capture; its text by tesseract
    must(cond, 'what')                   stops the tour at the first step that failed (TourStop)

WHAT WAS LEARNED DRIVING IT (15 Nov 2026)
  - About one press in eight is lost by a program that waits in a GETKEY + MOUSE loop, whatever the length of the
    press (diagnostics/KeyProbe_beta1.txt measured it; WAIT(-1) and Home lose none).  So every step must be checked:
    act() and pick() look for a change of the screen and send the press again when there is none.  A press that
    rightly changes nothing (Down on the last row) is sent with must_change=False.
  - Keys sent on after a missed step go anywhere: Enter in the Program Catalog opens the EDITOR of the highlighted
    program, and digits typed then go into its text.  A tour stops at the first miss (must).
  - The Program Catalog lists the program touched last first, and scrolls by pixels: rows are found where they are
    (catalog_state), never by a fixed grid, and the highlight is moved with the arrow keys.  A tap on a row that is
    not highlighted opens its editor at once.
  - In an INPUT form with one field, Enter after the typed value closes the form.
  - Two looks that are the same 0.6 s apart mean the page has settled; the clock corner is left out of the comparison.

The emulator's window stands at +320+272; with the small skin (3_Prime_small) its 320 x 240 screen is at (323, 339).
A click is held for a moment, since a quick one can be missed by a GETKEY + MOUSE loop (Lessons Learned s16).
"""
import os, subprocess, time, re
os.environ['DISPLAY'] = ':99'
SX, SY = 323, 339                      # the calculator screen's top left corner on the X display
KEYS = {                               # the skin's keys, at their X display places
    'Apps': (345, 624), 'Home': (345, 670), 'Symb': (399, 617), 'Plot': (399, 646), 'Num': (399, 677),
    'Help': (564, 617), 'View': (564, 646), 'Menu': (564, 677), 'Esc': (620, 624), 'CAS': (620, 670),
    'Up': (483, 615), 'Down': (483, 681), 'Left': (450, 648), 'Right': (517, 648),
    'Vars': (345, 725), 'Toolbox': (399, 725), 'Del': (620, 725), 'Enter': (592, 816),
    '7': (407, 861), '8': (482, 861), '9': (558, 861), 'Div': (620, 861),
    'Alpha': (345, 907), '4': (407, 907), '5': (482, 907), '6': (558, 907), 'Times': (620, 907),
    'Shift': (345, 952), '1': (407, 952), '2': (482, 952), '3': (558, 952), 'Minus': (620, 952),
    'On': (345, 997), '0': (407, 997), 'Dot': (482, 997), 'Space': (558, 997), 'Plus': (620, 997),
}
SOFT = {1: (26, 228), 2: (80, 228), 3: (133, 228), 4: (186, 228), 5: (240, 228), 6: (293, 228)}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def click(x, y, hold=0.35):
    sh('xdotool', 'mousemove', str(x), str(y)); time.sleep(0.08)
    sh('xdotool', 'mousedown', '1'); time.sleep(hold); sh('xdotool', 'mouseup', '1')


def tap(cx, cy, hold=0.35):
    click(SX + cx, SY + cy, hold)


def soft(n, hold=0.35):
    tap(*SOFT[n], hold=hold)


def key(name, hold=0.35):
    click(*KEYS[name], hold=hold)


def cap(path, x3=False):
    a = ['import', '-window', 'root', '-crop', '320x240+%d+%d' % (SX, SY), '+repage']
    if x3:
        a += ['-filter', 'point', '-resize', '300%']
    sh(*(a + [path]))
    return path


def ocr(path, crop=None, psm=6):
    """text of a 320 x 240 capture (or of crop = (w, h, x, y) of it), enlarged four times for tesseract"""
    tmp = path + '.ocr.png'
    a = ['convert', path]
    if crop:
        a += ['-crop', '%dx%d+%d+%d' % crop, '+repage']
    a += ['-filter', 'Lanczos', '-resize', '400%', '-colorspace', 'Gray', tmp]
    sh(*a)
    r = sh('tesseract', tmp, '-', '--psm', str(psm))
    try: os.remove(tmp)
    except OSError: pass
    return r.stdout.strip()


def pixel(path, x, y):
    r = sh('convert', path, '-format', '%%[pixel:p{%d,%d}]' % (x, y), 'info:')
    return r.stdout.strip()


def alive():
    return sh('pgrep', '-f', 'HPPrime.ex').returncode == 0


def norm(s):
    return re.sub(r'[^A-Za-z0-9]', '', s)


# ---------------------------------------------------------------- tours (Round 16)
import hashlib, sys, difflib
TMP = os.path.join(os.environ.get('VC', '/tmp/vc'), 'tmp') + os.sep       # scratch pictures; VC = the cloud calculator's folder
os.makedirs(TMP, exist_ok=True)


def grab():
    """the screen's pixels (clock corner blanked) as a digest, for comparing two moments"""
    from PIL import Image
    p = TMP + 'g.png'
    sh('import', '-window', 'root', '-crop', '320x240+%d+%d' % (SX, SY), '+repage', p)
    im = Image.open(p).convert('RGB')
    im.paste((0, 0, 0), (270, 0, 320, 20))
    return hashlib.md5(im.tobytes()).hexdigest()


def settle(timeout=20.0, quiet=0.6, first=0.3):
    """wait until the screen stops changing: two looks `quiet` seconds apart that are the same"""
    time.sleep(first)
    t0 = time.time(); a = grab()
    while time.time() - t0 < timeout:
        time.sleep(quiet)
        b = grab()
        if a == b:
            return True
        a = b
    return False


def changed(before, timeout=15.0, step=0.3):
    """wait until the screen differs from `before` (a grab()); True if it did"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        if grab() != before:
            return True
        time.sleep(step)
    return False


def act(fn, *a, wait=20.0, must_change=True, retry=3, **kw):
    """do one key or tap, then wait for the screen to change and to stop changing.  When nothing changed the press is
    sent once more (a press can be lost while a page draws); returns False when nothing changed either time."""
    for attempt in range(1 + (retry if must_change else 0)):
        b = grab()
        fn(*a, **kw)
        ch = changed(b, timeout=6.0 if must_change else 1.5)
        settle(timeout=wait)
        if ch or not must_change:
            return ch
        print('   (no change after %s%s: sent again)' % (getattr(fn, '__name__', '?'), a), flush=True)
    return False


def pick(n, wait=20.0, retry=3):
    """choose item n of an open CHOOSE box: its digit for 1-9, Downs and Enter above that (the box opens on item 1).
    A digit that changes nothing is sent again (a press can be lost); the Downs are counted on the screen."""
    if n <= 9:
        for attempt in range(1 + retry):
            b = grab()
            key(str(n))
            if changed(b, timeout=6.0):
                settle(timeout=wait)
                return True
            print('   (no change after digit %d: sent again)' % n, flush=True)
        return False
    for _ in range(n - 1):
        for attempt in range(1 + retry):
            b = grab()
            key('Down', hold=0.2)
            if changed(b, timeout=2.5):
                break
            print('   (a Down in the menu changed nothing: sent again)', flush=True)
        time.sleep(0.25)
    b = grab()
    key('Enter')
    ch = changed(b, timeout=6.0)
    settle(timeout=wait)
    return ch


def title_text(path=None):
    p = path or cap(TMP + 'title.png')
    best = ''
    for crop in ((200, 20, 60, 0), (320, 20, 0, 0)):
        for neg in (True, False):
            a = ['convert', p, '-crop', '%dx%d+%d+%d' % crop, '+repage']
            if neg: a.append('-negate')
            sh(*(a + [TMP + 'title_n.png']))
            for psm in (7, 6, 13):
                t = ocr(TMP + 'title_n.png', None, psm)
                if 'Main' in t or 'Catalog' in t or 'Function' in t:
                    return t
                if len(t) > len(best): best = t
    return best


def like(text, name):
    t = norm(text).lower(); n = name.lower(); best = 0
    for i in range(0, max(1, len(t) - len(n) + 1)):
        best = max(best, difflib.SequenceMatcher(None, t[i:i + len(n)], n).ratio())
    return best


def catalog():
    """open the Program Catalog (Shift, 1) from Home or from the catalog itself"""
    key('Shift'); time.sleep(0.6); key('1'); settle(15)
    return 'Catalog' in title_text()


class TourStop(Exception):
    pass


def must(cond, what):
    """stop a tour at the first step that did not do what it should (keys sent on after a miss go anywhere)"""
    if not cond:
        cap(TMP + 'stop.png')
        raise TourStop(what)
    return cond


def catalog_state():
    """the Program Catalog as it stands: [(name text, y)], the highlighted row's y (or None).  Rows are found where they
    are (the list scrolls by pixels), names by reading the whole list once."""
    from PIL import Image
    p = cap(TMP + 'cat.png')
    im = Image.open(p).convert('RGB')
    ys = [y for y in range(21, 219) if im.getpixel((200, y)) == (173, 204, 255)]
    hi = (min(ys) + max(ys)) / 2.0 if ys else None
    sh('convert', p, '-crop', '250x199+0+21', '+repage', '-filter', 'Lanczos', '-resize', '400%', '-colorspace', 'Gray',
       TMP + 'cat4.png')
    r = sh('tesseract', TMP + 'cat4.png', '-', '--psm', '6', 'tsv')
    lines = {}
    for ln in r.stdout.splitlines()[1:]:
        f = ln.split('\t')
        if len(f) < 12 or not f[11].strip():
            continue
        key_ = (f[2], f[3], f[4])
        top, h = int(f[7]), int(f[9])
        lines.setdefault(key_, []).append((f[11], top + h / 2.0))
    rows = []
    for k_, ws in lines.items():
        rows.append((' '.join(w for w, _ in ws), 21 + sum(c for _, c in ws) / len(ws) / 4.0))
    rows.sort(key=lambda t: t[1])
    return rows, hi


def run_program(name, softkey=6):
    """in the Program Catalog: move the highlight to the program's row with the arrow keys, then Run (soft key 6;
    soft key 1 is Edit).  Returns True when the key was pressed on a row whose name reads as `name`."""
    for _ in range(16):
        rows, hi = catalog_state()
        if hi is None:
            return False
        want = [y for t, y in rows if like(t, name) >= 0.8]
        if not want:
            key('Down', hold=0.2); time.sleep(0.8)          # not in sight: scroll on
            continue
        d = want[0] - hi
        if abs(d) < 8:
            soft(softkey)                                    # Run (or Edit)
            return True
        key('Down' if d > 0 else 'Up', hold=0.2); time.sleep(0.8)
    return False

# -*- coding: utf-8 -*-
"""Round 17 (17 Nov 2026): the programs' screen text follows the book's two rules for a statistic's letter, as far as a
screen can.

Roger, 17 Nov 2026, reading Draft 46 of the book: "The p-value and t-test, t-distribution etc should be hyphenated and
italicized" and "make sure expressions like n-1 are in parentheses"; then, asked whether the programs' own text should
follow (the book prints their help pages word for word): "Now, as Round 17".  A calculator's screen has no italics, so a
program keeps the other half of each rule (tools/screen_text_v1.py is the check, and says what is left alone):

  (a) an expression like n - 1 stands in parentheses of its own:  df = (n - 1),  (k - 1) df,  df = (N1 + N2 - 2);
  (b) a hyphen joins a statistic's letter to its noun:  F-test, z-test, t-curve, t-interval, t-table, F-quantiles ...;
  (c) the p of p-value is a small letter, at the start of a title too.

Fifteen programs are built here, each from the version before (read from git, BASE) by exact replacements INSIDE QUOTED
STRINGS ONLY: a replacement is looked for in the code of each line, never in its comment, and must be found the number of
times EDITS says, or the build stops.  Comments keep their wording: they are not on the screen.  The sixteenth,
TTestLabG beta 1i, is built from TTestLab beta 1l by tools/make_tlg1_v4.py (the general version is always built from the
advanced one), which this script runs last.

Run from the repository's root:    python3 verify/round17/make_round17.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap

BASE = '39bb935'                     # main before Round 17
DATE = '17 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r17_programs'
S1, S2, S0 = u'₁', u'₂', u'₀'         # subscripts, as the programs' strings hold them
X2, MU, SG = u'χ²', u'μ', u'σ'   # chi-square, mu, sigma

# name: (old version, new version, [(old text, new text, how many times in the code)], what the history note says)
EDITS = {
 'AgreeLab': ('beta1h', 'beta1i', [
   ('"ICC intervals (F quantiles)"', '"ICC intervals (F-quantiles)"', 1),
   ('"no F interval', '"no F-interval', 6)],
   '"F-quantiles" in the waiting message of the ICC intervals and "no F-interval" in the six notes of an ICC whose '
   'interval cannot be had (they said "F quantiles", "no F interval").'),
 'AnovaLab': ('beta1i', 'beta1j', [
   ('"The q distribution is an integral, done here"', '"The q-distribution is an integral, done here"', 1),
   ('" is true, F is near 1 and follows the"', '" is true, F is near 1 and follows the F-curve"', 1),
   ('"F(k - 1, N - k) curve; p = P(F this big | "', '"with (k - 1) and (N - k) df; p = P(F this big | "', 1),
   ('"The F test assumes equal spreads', '"The F-test assumes equal spreads', 1),
   ('(a placebo, the usual method): k - 1 comparisons,"', '(a placebo, the usual method): (k - 1) comparisons,"', 1),
   ('", df n - 1."', '", df = (n - 1)."', 1),
   ('", df n" + avS1 + " - 1 and n" + avS2 + " - 1."', '", df = (n" + avS1 + " - 1) and (n" + avS2 + " - 1)."', 1),
   ('"F curve and p"', '"F-curve and p"', 1),
   ('"F curve of an effect"', '"F-curve of an effect"', 1),
   ('"F curve (treatments)"', '"F-curve (treatments)"', 1),
   ('": the F test and interval"', '": the F-test and interval"', 1)],
   'Help 1 of 10: "follows the F-curve with (k - 1) and (N - k) df" (it said "follows the F(k - 1, N - k) curve").  '
   'Help 5: "(k - 1) comparisons".  Help 8: "df = (n - 1)" and "df = (n1 - 1) and (n2 - 1)" (they said "df n - 1", '
   '"df n1 - 1 and n2 - 1").  "F-test", "F-curve" and "q-distribution" with a hyphen: help 2 of 10, the waiting page '
   'of Tukey\'s studentized range, the band of the two-variance result, and one item in each of the three page '
   'menus ("F-curve and p", "F-curve of an effect", "F-curve (treatments)"); the items keep their numbers.'),
 'CICatcher': ('beta2l', 'beta2m', [
   ('(a t interval needs 2 or more)', '(a t-interval needs 2 or more)', 1)],
   'The sentence that refuses a sample size outside 2 to 100 says "a t-interval needs 2 or more" (it said "a t '
   'interval").'),
 'EpiStats': ('v1.7l', 'v1.7m', [
   ('"M-H ' + X2 + ' (1 df): is the common OR 1?"', '"M-H ' + X2 + ', 1 df: is the common OR 1?"', 1),
   ('"Breslow-Day (k-1 df): are the strata\'s ORs alike?  A small p"',
    '"Breslow-Day, (k-1) df: are the strata\'s ORs alike?  A small p"', 1)],
   'Help 6 of 15 (Mantel-Haenszel): "Breslow-Day, (k-1) df:" (it said "Breslow-Day (k-1 df):"), and the line above '
   'it in the same form, "M-H chi-square, 1 df:" (it said "(1 df):").'),
 'ExhibitLab': ('beta1h', 'beta1i', [
   ('"SD (divisor n - 1), grams, 0 to 1,000"', '"SD, divisor (n - 1), grams, 0 to 1,000"', 1),
   ('" t SE, t on n - 1",', '" t SE, t on (n - 1)",', 1)],
   'Help 4 of 8: "t on (n - 1) df" (it said "t on n - 1 df"); the help line of the SD field of the weights form: "SD, '
   'divisor (n - 1), grams, 0 to 1,000" (it said "SD (divisor n - 1), ...").'),
 'FitCheck': ('beta1i', 'beta1j', [
   ('"(k - 3) and " + fcX2S + "(k - 1) (Chernoff & Lehmann 1954); df = k - 3 is the usual textbook rule."',
    '"(k-3) and " + fcX2S + "(k-1) (Chernoff & Lehmann 1954); df = (k-3) is the usual textbook rule."', 1),
   ('"df = k - 1 - m = "', '"df = (k-1-m) = "', 3),
   ('One parameter estimated: df = k - 2."', 'One parameter estimated: df = (k-2)."', 1),
   ('": one parameter estimated, df = k - 2."', '": one parameter estimated, df = (k-2)."', 1),
   ('" was given, not estimated: df = k - 1."', '" was given, not estimated: df = (k-1)."', 1),
   ('Two parameters estimated: df = k - 3."', 'Two parameters estimated: df = (k-3)."', 1),
   ('the estimates and the cells match and df = k - 3."', 'the estimates and the cells match and df = (k-3)."', 1),
   ('the sparse tails are merged, df = k - 3."', 'the sparse tails are merged, df = (k-3)."', 1),
   ('"p is estimated from the data, so df = k - 2."', '"p is estimated from the data, so df = (k-2)."', 1),
   ('are far from E.  df = k - 1 - m, where m counts', 'are far from E.  df = (k-1-m), where m counts', 1),
   ('so the E add up to N; df = k - 2.  BINOMIAL: p estimated (df = k - 2) or typed (df = k - 1)."',
    'so the E add up to N; df = (k-2).  BINOMIAL: p estimated, df = (k-2); typed, df = (k-1)."', 1),
   ('" on bins: df = k - 3.  "', '" on bins: df = (k-3).  "', 1)],
   'The degrees of freedom stand in parentheses wherever a page writes them out: "df = (k-1-m)" (the curve page, in '
   'both of its forms, the working lines of the test page, and help), "df = (k-2)", "df = (k-1)" and "df = (k-3)" '
   '(the working lines of the Poisson, binomial and normal fits, the two notes of a normal fit to bins, two '
   'data-source pages, and help).  They are written without spaces because most of these sentences flow from line '
   'to line, and the wrap breaks a line at a space: the old "df = k - 3" could end one line at "k -" and begin the '
   'next with "3."; "(k-3)" stays whole.  For the same reason the note on raw values in bins writes "chi-square(k-3) '
   'and chi-square(k-1)".  One help sentence was turned so that no parenthesis stands inside another: "BINOMIAL: p '
   'estimated, df = (k-2); typed, df = (k-1)."  No text is longer than it was, so no page gains a line.'),
 'PowerViz': ('v2.5s', 'v2.5t', [
   ('"F test of s' + S1 + u'²/s' + S2 + u'² (exact, normal data): "', '"F-test of s' + S1 + u'²/s' + S2 + u'² (exact, normal data): "', 1),
   ('"The F test of s' + S1 + u'²/s' + S2 + u'² ("', '"The F-test of s' + S1 + u'²/s' + S2 + u'² ("', 1),
   ('the program puts in the z values (PPL), giving"', 'the program puts in the z-values (PPL), giving"', 1),
   ('"z test: ' + SG + S1 + ', ' + SG + S2 + ' taken as known.', '"z-test: ' + SG + S1 + ', ' + SG + S2 + ' taken as known.', 1)],
   '"F-test" on the two pages of "Would Levene\'s test notice?", "z-values" on help 5 of 7 and "z-test:" on help 6 of '
   '7 (they said "F test", "z values", "z test").'),
 'RankLab': ('beta1j', 'beta1k', [
   ('"magenta = the p tail(s)', '"magenta = the p-tail(s)', 2)],
   'The legend under the null-distribution plot says "the p-tail(s)" (it said "the p tail(s)"), in both of its forms.'),
 'ResampLab': ('beta1i', 'beta1j', [
   ('"Compare the percentile, BCa and t intervals."', '"Compare the percentile, BCa and t-intervals."', 1)],
   'The note of the example "months served" says "the percentile, BCa and t-intervals" (it said "t intervals").'),
 'ScatterLab': ('beta2l', 'beta2m', [
   ('",  df = n - 2 = "', '",  df = (n - 2) = "', 1),
   ('"  df = n - 2;  H"', '"  df = (n - 2);  H"', 1)],
   'The inference page writes "df = (n - 2) = ..." and help 7 of 7 "df = (n - 2);" (they said "df = n - 2").'),
 'StudRange': ('beta15m', 'beta15n', [
   ('"P-value from q"', '"p-value from q"', 2),
   ('"P-value: Studentized Range"', '"p-value: Studentized Range"', 1)],
   'The first item of the main menu, the title of its form and the title of its result page say "p-value" with a '
   'small p (they said "P-value"), as ChiTable, EpiStats and AgreeLab do and as the book writes it.'),
 'TDist3D': ('beta1a', 'beta1b', [
   ('"Student\'s t has one parameter, the degrees of freedom " + tdNS + " = n " + tdMin + " 1."',
    '"Student\'s t has one parameter: degrees of freedom, " + tdNS + " = (n " + tdMin + " 1)."', 1),
   ('"Every t curve at once: t runs across, the degrees"', '"Every t-curve at once: t runs across, the degrees"', 1)],
   'Help 1 of 4: "Student\'s t has one parameter: degrees of freedom, nu = (n - 1)." (it said "... one parameter, the '
   'degrees of freedom nu = n - 1."; with the parentheses the old sentence was 299 pixels wide at the glyph widths '
   'measured on the Virtual Calculator, and the line holds 296: the new one is 285).  The opening page says "Every '
   't-curve at once" (it said "t curve").'),
 'TTestLab': ('beta1k', 'beta1l', [
   ('"Pooled variances:  df = N"+CHAR(8321)+" + N"+CHAR(8322)+" - 2"', '"Pooled variances:  df = (N"+CHAR(8321)+" + N"+CHAR(8322)+" - 2)"', 1),
   ('"t table, row df = "', '"t-table, row df = "', 1),
   ('"One sample:  df = N - 1"', '"One sample:  df = (N - 1)"', 1),
   (' - ' + MU + S0 + u')/(s/√N), df = N - 1.  Type the mean, SD and N,"', ' - ' + MU + S0 + u')/(s/√N), df = (N - 1).  Type the mean, SD and N,"', 1)],
   'Step 2 writes "Pooled variances:  df = (N1 + N2 - 2)" and "One sample:  df = (N - 1)"; step 3 says "t-table, row '
   'df = ..."; help 3 of 3 says "df = (N - 1)" (they said "df = N1 + N2 - 2", "df = N - 1", "t table").'),
 'TestChooser': ('beta2g', 'beta2h', [
   ('"Cochran\'s Q test"', '"Cochran\'s Q-test"', 1),
   ('"Extends McNemar; ' + X2 + ', k - 1 df."', '"Extends McNemar; ' + X2 + ', (k - 1) df."', 1),
   ('"Rank one-way ANOVA; ' + X2 + ', k - 1 df."', '"Rank one-way ANOVA; ' + X2 + ', (k - 1) df."', 1),
   ('"Rank repeated-measures ANOVA; k - 1 df."', '"Rank repeated-measures ANOVA; (k - 1) df."', 1),
   ('"' + X2 + ', k - 1 df; prop. hazards."', '"' + X2 + ', (k - 1) df; prop. hazards."', 1)],
   'The test in cell 9 is named "Cochran\'s Q-test" (it said "Cochran\'s Q test"), and four detail lines write '
   '"(k - 1) df" (they said "k - 1 df"): Cochran\'s Q, Kruskal-Wallis, Friedman and the log-rank test for several '
   'groups.'),
 'TrendTest': ('beta3m', 'beta3n', [
   ('"Departure = Pearson - trend, k-2 df"', '"Departure = Pearson - trend, (k-2) df"', 1),
   ('trChi + " (k-1 df) asks only', 'trChi + ", (k-1) df, asks only', 1),
   ('" (k-2 df) measures how far the"', '", (k-2) df, measures how far the"', 1)],
   'Help 1 of 3 writes "Pearson\'s chi-square, (k-1) df, asks only ..." and "... minus the trend chi-square, (k-2) df, '
   'measures ..." (they said "(k-1 df)", "(k-2 df)"); the formulas under the odds ratios write "(k-2) df" (it said '
   '"k-2 df").'),
}


def tag(v):
    return v.replace('beta', 'beta ')


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def split_comment(line):
    """(code, comment): the line cut at the first // that is outside a quoted string"""
    q = False
    for i, ch in enumerate(line):
        if ch == '"':
            q = not q
        elif not q and line[i:i + 2] == '//':
            return line[:i], line[i:]
    return line, ''


def edit_code(name, s, eds):
    """each replacement, in the code of each line only (never in a comment), found exactly the number of times named"""
    L = [split_comment(l) for l in s.split('\n')]
    for a, b, want in eds:
        got = sum(c.count(a) for c, _ in L)
        if got != want:
            die('%s: %d matches in the code (wanted %d) for %r' % (name, got, want, a[:70]))
        L = [(c.replace(a, b), k) for c, k in L]
    return '\n'.join(c + k for c, k in L)


def bump(name, s, ov, nv, note):
    """Round 11's bump: the header line, a history note before the old version's, and every version string in a literal."""
    ot, nt = tag(ov), tag(nv)
    L = s.split('\n')
    hv = None
    for i, l in enumerate(L[:40]):
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(ot) + r'\b', l):
            hv = i
            break
    if hv is None:
        die(name + ': no header line for ' + ot)
    L[hv] = L[hv].replace(ot, nt)
    L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(%s)' % DATE, L[hv], count=1)
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist:
        die(name + ': no history line for ' + ot)
    body = ('Round 17: the screen text follows the book\'s two rules for a statistic\'s letter as far as a screen can '
            '(Roger, 17 Nov 2026: "The p-value and t-test, t-distribution etc should be hyphenated and italicized"; '
            '"make sure expressions like n-1 are in parentheses").  ' + note + '  Only text inside quotation marks '
            'changed, and the version: no statement, number or name.  tools/screen_text_v1.py is the check.')
    L.insert(hist[0], '// %s (%s): ' % (nt, DATE) + '\n//   '.join(textwrap.wrap(body, 100)))
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
    # a version on screen with its date: the new date (Round 11's bump did the same)
    s = re.sub(r'"[^"\n]*%s[^"\n]*"' % re.escape(nt), lambda m: re.sub(r'\b\d{1,2} Nov 2026', DATE, m.group(0)), s)
    return s


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, name, ov)], check=True,
                          capture_output=True).stdout.decode('utf-8')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, (ov, nv, eds, note) in EDITS.items():
        s = edit_code(name, old_text(name, ov), eds)
        s = bump(name, s, ov, nv, note)
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-11s %s -> %s  (%d places)' % (name, ov, nv, sum(e[2] for e in eds)))
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.dirname(here)), 'tools', 'make_tlg1_v4.py'),
                        os.path.join(OUT, 'TTestLab_beta1l.txt'), OUT], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        die('tools/make_tlg1_v4.py: ' + (r.stderr or r.stdout).strip()[-300:])

# NormExplorer beta 42a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 42; every beta 42 feature is kept. Run on the PC harness (ppl_run_v3e) only: not yet on the Virtual Calculator or on hardware.*
*"Old" line numbers are `NormExplorer_beta42.txt`'s (3418 lines); "new" are `NormExplorer_beta42a.txt`'s (3706 lines).*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2, items 8 and 12; `findings_D.md`, section 1) found:

- **D-NE-1** (wrong text): "the scientific form on screen (104 `STRING(x,2,d)` sites, 0 `STRING(ROUND…)`). NormExplorer beta 42 is dated 16 Oct; the ᴇ finding is 17 Oct and the sweep went into ChiTable 3c, ScatterLab 2b and the ten 18-Oct programs, not here." Probability from x, right tail, x = 180 on N(100, 15) printed `P(X > x) = 4.8213ᴇ−8`; the Explorer `area to the left = 1.2934ᴇ−9`; a tapped outer bar `1.1ᴇ−2 expected (n×p)` and `p = 5.6746ᴇ−5`; a percentile at 1E-9 `1.0ᴇ−7% of the distribution falls below x`; C = 0.9999 `each tail 5.00ᴇ−3%`.
- **D-NE-2** (wrong number, Home export): "`1 − NORMALD_CDF` at 12 digits … `NE_P` for a right tail is exactly 0 on the Prime once x > μ + 7σ."
- **D-NE-3** (cosmetic): "CHOOSE return values tested — 1453, 1531, 1614, 1809, 1921, 1971, 1988."
- **D-NE-4** (cosmetic): "C = 1 is refused … 'Central proportion: .95 or 95 both work'; a typed 1 (meaning 1%) falls through `IF icC > 1` and is refused."
- **D-NE-5** (cosmetic): "the Explorer's μ step is fitted to σ at entry … After a σ drag from 15 to 2 the arrows still move μ by 5."

Decision D15 (tiny areas as `0.0000` or `< 0.0001`) is open. Per BRIEF_FIX19 this version applies the honest minimum: a value that is positive but would round to zero prints `< 0.0001`, never `0.0000` and never in scientific form.

Also, at Roger's request (19 Oct 2026, 12:48): the DISCLAIMER line under the distribution terms. And, at the coordinator's request (19 Oct 2026), the two tail problems found while verifying D-NE-2: an area between two x's far above the mean (item 7), and right-tail quantiles formed from 1 − α (item 8).

## What changed (line numbers: beta 42 → beta 42a)

1. **Four helpers** (new 670-735, after `ne_NiceNum`; forward declarations new 476-479). Every non-EXPORT name carries the `ne_` tag.
   - `ne_Fx(v, d)` (683-689) rounds before `STRING(…, 2, d)`. The rounded value is then 0 or at least 10⁻ᵈ, so the fixed form holds, and a negative value that rounds to 0 is set to a plain 0 (no `−0.0000`). This is ScatterLab 2b's `slFx`.
   - `ne_PStr(v, d)` (698-704) is for anything that cannot be negative: an area, a density, σ, s, an expected count, a width. When the value is positive but `ROUND(v, d)` is 0, it returns `"< 0.0001"` (d = 4; `"< 0.01"` for d = 2, `"< 0.000001"` for d = 6). Otherwise it calls `ne_Fx`. The findings' one-argument `ne_PStr(p)` gained the decimals argument, so σ at 2 decimals and an expected count at 1 decimal follow the same rule.
   - `ne_Eq(s)` (711-717) returns `" = " + s`, or `" " + s` when s starts with `<`. The screen reads `P(X > x) < 0.0001`, never `P(X > x) = < 0.0001`. This is Norm3 v2.4a's `n3_Eq` and BayesTree 8d's `bt_Eq` (Roger approved that rule on 17 Oct). It reads `LEFT(s, 1)` only inside `IF DIM(s) > 0`.
   - `ne_Btw(μ, σ, a, b)` (729-735; item 7) returns the area between a and b. When a > μ it computes `F(2μ − a) − F(2μ − b)`, the mirror image; otherwise `F(b) − F(a)`. The comment above it (719-728) explains why.
2. **D-NE-1, the sweep.** All 134 `STRING(x, 2, d)` calls of beta 42 now go through a helper. They sit on 111 lines; the review counted 104, and the table below lists every one. 86 calls use `ne_Fx`, 13 use `ne_PStr`, and 35 use `ne_PStr` inside `ne_Eq`. The one `STRING` call left in the code is inside `ne_Fx`. Where `ne_Eq` now supplies " = ", the label lost its own trailing " = ": the readouts at old 3265, 3267, 3285, 3287, 3300 and 3302 (new 3535, 3537, 3555, 3557, 3577 and 3579). Signed values (x, z, μ, μ₂, d, x̄, the bounds, window edges, axis ticks) use `ne_Fx`, because 0.0000 is their correctly rounded value. Counts use `ne_Fx(n, 0)`, which prints the same as before.
3. **D-NE-2, right tails as lower tails.** `1 − NORMALD_CDF` is exactly 0 on the Prime once a tail is below about 5E-13. Every right tail is now the mirror-image lower tail, `NORMALD_CDF(μ, σ, 2μ − t)`:
   - the right-tail panel and `NE_P`: 1556 → 1746;
   - the left-tail panel's complement P(X > x): 1554 → 1743-1744;
   - the right-tail panel's complement, P(X < x), read directly as `NORMALD_CDF(μ, σ, x)` rather than 1 − NE_P: 1561 → 1751-1752;
   - the outside area, as a new local `pcO = F(a) + F(2μ − b)` (set at new 1775): used for `NE_P` (1587 → 1787) and on both panels (1585 → 1785, 1592 → 1792);
   - power, `F(μ₂, σ, 2μ₂ − x*)`: 1945 → 2185;
   - β, read directly as `F(μ₂, σ, x*)` rather than 1 − power: 1955 → 2199-2200;
   - the plot readouts: one tail 3254 → 3524, outside 3295 → 3570-3572, power 3324 → 3603;
   - the riding tags: 3342 → 3624 and 3351 → 3633.

   The review's site list was 1556, 1945, 3254, 3324, 3342 and 3351. I added the two complements, the outside area and β: each is a tail computed through `1 −` and printed on the same panels, so each read 0.0000 the same way. Mode 4's `1 − (F(b) − F(a))`, which the review called fine, also lost the right tail's digits. In the harness it was 46 % off at ±8σ, and on the Prime it is 0.
4. **D-NE-3, the CHOOSE idiom.** At 1453, 1531, 1614, 1809, 1921, 1971 and 1988 (new 1622, 1706, 1817, 2036, 2155, 2219 and 2237), `CHOOSE(idx, …);` is a statement and the test that follows is `IF idx == 0 THEN RETURN; END;`. The tests were at 1463, 1536, 1620, 1814, 1925, 1979 and 1990 (new 1632, 1711, 1823, 2041, 2159, 2227 and 2239). The locals `swSel`, `pcSel`, `icSel`, `zsSel`, `c2Sel` and `hsSel` are gone from their LOCAL lines (1437, 1529, 1608, 1801, 1919 and 1969 → 1603, 1701, 1808, 2025, 2150 and 2214). `pcO` took `pcSel`'s place. Each index was already set to 0 before its CHOOSE. A comment above each CHOOSE says why; none sits inside a bracket.
5. **D-NE-4**: 1725 → 1940-1944. `IF icC >= 1 THEN icC := icC / 100; END;` reads a typed 1 as 1 %, which the help line's ".95 or 95 both work" implies. A typed 100 becomes 1 and is still refused.
6. **D-NE-5**: 1236 → 1394-1402. On the lift after a σ drag, `exS0`, `exStep` and `exSStep` refit to the snapped σ, exactly as Centre does (1315-1317). The bound step `exBStp` is left alone, since Centre does not refit it either; see Unresolved.
7. **"Between", mirrored** (found while verifying D-NE-2; fixed at the coordinator's request). When both bounds are past about 7σ above the mean, both CDFs are exactly 1 on the Prime, so `F(b) − F(a)` printed 0.0000. The same difference also appeared for a histogram bar's p when the curve was moved far to the left of the bars. All four sites now call `ne_Btw`:
   - the Probability-between panel: 1575 → 1766-1769;
   - the plot readout: 3294 → 3564-3566;
   - the riding tag: 3346-3347 → 3628-3629;
   - a bar's p and expected count: 3365-3366 → 3647-3650.

   An area that straddles or lies below the mean uses the plain difference. That is already accurate there, and its result is unchanged to the last digit (checked).
8. **Right-tail quantiles without 1 − α** (same request). Φ⁻¹(1 − p) is exactly −Φ⁻¹(p). For a typed α below about 5E-13, 1 − α is 1 on the Prime, and `NORMALD_ICDF(0, 1, 1)` is not a number; the review's §5 question is whether that is an error or ∞. Four sites now take minus the quantile of the small area:
   - the right-tail critical value: 1654 → 1861-1866, `−NORMALD_ICDF(0, 1, α)`;
   - the two tails: 1705 → 1917-1920, `−NORMALD_ICDF(0, 1, α/2)`;
   - the central interval: 1730 → 1949-1954, `−NORMALD_ICDF(0, 1, (1 − C)/2)`. For C = 0.999999999999, `(1 + C)/2` needed 13 digits and rounded to exactly 1;
   - the power picture's cut: 1944 → 2178-2181, `x* = μ − σ·NORMALD_ICDF(0, 1, α)`.

   I checked all six `NORMALD_ICDF` calls against the inputs their forms accept:
   - the percentile (`icP`) and the left tail (α) take the typed area, which each form refuses unless it is strictly between 0 and 1;
   - the four above take an area in (0, 1) or (0, 0.5).

   A minus before a built-in is the form `-FLOOR(LOG(...))` that this file and the fleet have run on hardware.
9. **Header.**
   - The banner says beta 42a at line 2 and line 75 (now 87).
   - The DISCLAIMER sits under the distribution terms (new 16-18): "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." No page of the program states the terms (Help has three pages: the modules, the soft keys, touch), so no page changed with it.
   - The tested-on lines (16-19 → 20-26) say that beta 42 ran on the Virtual Calculator and that beta 42a has run on the PC harness only.
   - The guide line (24 → 31-33) names `normexplorer-guide_beta42.md` as written for beta 42.
   - The file map has the true count, 3706 lines, and lines for the helpers.
   - A dated "beta 42a (19 Oct 2026)" paragraph (new 91-164), items (1)-(8), cites D-NE-1 to D-NE-5 and the two tail items, with beta 42's line numbers.

**Before and after** (harness ppl_run_v3e, `home_minus=True`; every row is run in the verify script on both files):

| Where | beta 42 | beta 42a |
|---|---|---|
| Probability from x, right tail, x = 180 on N(100,15): panel, view | `P(X > x) = 4.8213ᴇ−8`, `P(X > x₀) = 4.8213ᴇ−8` | `P(X > x) < 0.0001`, `P(X > x₀) < 0.0001` |
| Explorer, x₀ dragged to the left edge (N(0,1)) | `area to the left = 1.2934ᴇ−9`, `height 7.909464ᴇ−9 (density,` | `area to the left < 0.0001`, `height < 0.000001 (density,` |
| Outermost histogram bar tapped | `1 observed, 1.1ᴇ−2 expected (n×p)`, `p = 5.6746ᴇ−5` | `1 observed, < 0.1 expected (n×p)`, `p = 0.0001` |
| Percentile, area 1E-9 | `area left = 1.0000ᴇ−9`, `1.0ᴇ−7% of the distribution falls below x` | `area left < 0.0001`, `< 0.1% of the distribution falls below x` |
| Central C = 0.9999 | `each tail 5.00ᴇ−3%` | `each tail < 0.01%` (PC doubles; the Prime's exact 0.005 rounds to `0.01%`) |
| z-solver, σ = 1E-5 | `σ = 1.0000ᴇ−5`, `…)/1.00ᴇ−5` | `σ < 0.0001`, `…)/< 0.01` |
| Window panel, σ = 1E5 | `y top = 4.5878ᴇ−6   peak = 3.9894ᴇ−6` | `y top < 0.0001   peak < 0.0001` |
| D2 message, s = 1E-8 | `s = 1.4901ᴇ−8` | `s < 0.0001` |
| Animation from σ = 0.001 | `σ = 1.00ᴇ−3`, bands `−1.00ᴇ−3…1.00ᴇ−3` | `σ < 0.01`, bands `0.00…0.00` |
| **12-digit model** (the Prime's built-ins): NE_P, right tail at z = 8 | `0` (`P(X > x) = 0.0000`) | `6.22096057427E-16` (`P(X > x) < 0.0001`) |
| 12-digit: left-tail panel at z = 8, complement | `Complement: P(X > x) = 0.0000` | `Complement: P(X > x) < 0.0001` |
| 12-digit: power picture, μ₂ = −8 on N(0,1) | `power = 0.0000`, NE_P 0 | `power < 0.0001`, NE_P 2.58424385419E-22 |
| 12-digit: power picture, μ₂ = 12 | `β = 0.0000` | `β < 0.0001` |
| 12-digit: right tail at 8σ, custom window 7..10 | readout `= 0.0000`, tag `0.0000` | readout `< 0.0001`, tag `< 0.0001` |
| Central, C = 1 | refused ("must be between 0 and 1") | `Central 1.0% interval`, z* = ± 0.0125 |
| Explorer: σ drag 15 → 2, then → and ↑ | μ 105, σ 4 | μ 100.5, σ 2.2 |
| 12-digit: between 9σ..12σ on N(100,15) (panel, view) | NE_P 0, `P(a < X < b) = 0.0000` | NE_P 1.1286E-19, `P(a < X < b) < 0.0001` |
| 12-digit: between 8.5..9.5 on N(0,1), window 8..10 (readout, tag) | `= 0.0000`, tag `0.0000` | `< 0.0001`, tag `< 0.0001` |
| 12-digit: bars tapped under N(−100, 15) (bars at 40..160) | `3 observed, 0.0 expected`, `p = 0.0000` | `3 observed, < 0.1 expected`, `p < 0.0001` |
| 12-digit: right-tail critical value, α = 1E-13 | stops at `NORMALD_ICDF(0, 1, 1)` | z* = 7.3488 |
| central interval, C = 0.999999999999 | on the Prime 1 + C rounds to 2, so it stops at `NORMALD_ICDF(0, 1, 1)`; the harness adds in doubles and gives a wrong z* = 7.0345 | z* = 7.1305 |
| Esc in any of the 7 menus | back to the main menu | the same |
| `NormExp` returned after x = 220 | `…, p = 6.6613ᴇ−16` (PC) / `p = 0.0000` (Prime) | `NormExp: z = 8.0000, x = 220.0000, p < 0.0001` |

**Left alone (checked):**
- **Areas just below 1** print `1.0000` (`Complement: P(X < x) = 1.0000`), and C = 0.9999 prints `Middle 100.0%`. Those are the ordinary rounding of the other side, and the brief's rule is about values that round to zero.
- **A computed 0** prints `0.0000`. In the Explorer, μ dragged 61σ from x₀ gives a tail of about 1E-810, which underflows to 0 on the PC (the Prime's range ends near 1E-499).
- **The axis labels** and the z-ruler went through `ne_Fx`. The step is at least 10⁻ᵈ, so they print as before; the rounding only guards a tick at 0 that carries a last-digit remainder.
- **The #PYTHON block** is byte-identical, so the CPython check was run only to confirm it.
- **Pending, as in beta 42:** the five `√`, `K` as the MAKELIST counter, and the program's own hex palette.

## Every STRING(x, 2, d) call of beta 42 (134), its category and its helper

Categories: probability (30), x value (61: x, z, a, b, the bounds, window edges and widths, bin edges), parameter (29: μ, σ, μ₂, d, x̄, s), axis (4), count (8, including the expected count n×p), density (2: the peak and the height at x₀, which the five suggested categories did not fit). `ne_PStr` (with `ne_Eq` after "label") is used for what cannot be negative; `ne_Fx` for the rest.

| Line old → new | beta 42 call | Category | beta 42a |
|---|---|---|---|
| 1503 → 1675 | `STRING(NE_WLO,2,3)` | x value | ne_Fx |
| 1504 → 1676 | `STRING(NE_WHI,2,3)` | x value | ne_Fx |
| 1505 → 1677 | `STRING(NE_WHI-NE_WLO,2,3)` | x value | ne_PStr, ne_Eq |
| 1506 → 1678 | `STRING((NE_WHI-NE_WLO)/NE_SG,2,2)` | x value | ne_PStr, ne_Eq |
| 1507 → 1679 | `STRING(NE_YMX,2,4)` | axis | ne_PStr, ne_Eq |
| 1508 → 1680 | `STRING(NORMALD(NE_MU,NE_SG,NE_MU),2,4)` | density | ne_PStr, ne_Eq |
| 1551 → 1740 | `STRING(pcA,2,4)` | x value | ne_Fx |
| 1552 → 1741 | `STRING(NE_Z,2,4)` | x value | ne_Fx |
| 1553 → 1742 | `STRING(NE_P,2,4)` | probability | ne_PStr, ne_Eq |
| 1554 → 1744 | `STRING(1-NE_P,2,4)` | probability | ne_PStr, ne_Eq |
| 1558 → 1748 | `STRING(pcA,2,4)` | x value | ne_Fx |
| 1559 → 1749 | `STRING(NE_Z,2,4)` | x value | ne_Fx |
| 1560 → 1750 | `STRING(NE_P,2,4)` | probability | ne_PStr, ne_Eq |
| 1561 → 1752 | `STRING(1-NE_P,2,4)` | probability | ne_PStr, ne_Eq |
| 1581 → 1781 | `STRING(pcA,2,4)` | x value | ne_Fx |
| 1581 → 1781 | `STRING(pcB,2,4)` | x value | ne_Fx |
| 1582 → 1782 | `STRING((pcA-NE_MU)/NE_SG,2,3)` | x value | ne_Fx |
| 1583 → 1783 | `STRING((pcB-NE_MU)/NE_SG,2,3)` | x value | ne_Fx |
| 1584 → 1784 | `STRING(pcP,2,4)` | probability | ne_PStr, ne_Eq |
| 1585 → 1785 | `STRING(1-pcP,2,4)` | probability | ne_PStr, ne_Eq |
| 1589 → 1789 | `STRING(pcA,2,4)` | x value | ne_Fx |
| 1589 → 1789 | `STRING(pcB,2,4)` | x value | ne_Fx |
| 1590 → 1790 | `STRING((pcA-NE_MU)/NE_SG,2,3)` | x value | ne_Fx |
| 1591 → 1791 | `STRING((pcB-NE_MU)/NE_SG,2,3)` | x value | ne_Fx |
| 1592 → 1792 | `STRING(1-pcP,2,4)` | probability | ne_PStr, ne_Eq |
| 1593 → 1793 | `STRING(pcP,2,4)` | probability | ne_PStr, ne_Eq |
| 1635 → 1842 | `STRING(icP,2,4)` | probability | ne_PStr, ne_Eq |
| 1636 → 1843 | `STRING(icZ,2,4)` | x value | ne_Fx |
| 1637 → 1844 | `STRING(icX,2,4)` | x value | ne_Fx |
| 1638 → 1845 | `STRING(100*icP,2,1)` | probability | ne_PStr |
| 1658 → 1870 | `STRING(icP,2,4)` | probability | ne_PStr, ne_Eq |
| 1659 → 1871 | `STRING(icZ,2,4)` | x value | ne_Fx |
| 1660 → 1872 | `STRING(icX,2,4)` | x value | ne_Fx |
| 1683 → 1895 | `STRING(icP,2,4)` | probability | ne_PStr, ne_Eq |
| 1684 → 1896 | `STRING(icZ,2,4)` | x value | ne_Fx |
| 1685 → 1897 | `STRING(icX,2,4)` | x value | ne_Fx |
| 1710 → 1925 | `STRING(icP,2,4)` | probability | ne_PStr, ne_Eq |
| 1710 → 1925 | `STRING(icP/2,2,4)` | probability | ne_PStr |
| 1711 → 1926 | `STRING(icZ,2,4)` | x value | ne_Fx |
| 1712 → 1927 | `STRING(icLO,2,4)` | x value | ne_Fx |
| 1712 → 1927 | `STRING(icHI,2,4)` | x value | ne_Fx |
| 1734 → 1958 | `STRING(100*icC,2,1)` | probability | ne_PStr |
| 1735 → 1959 | `STRING(icZ,2,4)` | x value | ne_Fx |
| 1736 → 1960 | `STRING(icLO,2,4)` | x value | ne_Fx |
| 1736 → 1960 | `STRING(icHI,2,4)` | x value | ne_Fx |
| 1737 → 1961 | `STRING(icLO,2,3)` | x value | ne_Fx |
| 1737 → 1961 | `STRING(icHI,2,3)` | x value | ne_Fx |
| 1738 → 1962 | `STRING(100*icC,2,1)` | probability | ne_PStr |
| 1739 → 1963 | `STRING(100*(1-icC)/2,2,2)` | probability | ne_PStr |
| 1828 → 2058 | `STRING(zsX,2,4)` | x value | ne_Fx |
| 1828 → 2058 | `STRING(zsM,2,4)` | parameter | ne_Fx |
| 1829 → 2059 | `STRING(zsS,2,4)` | parameter | ne_PStr, ne_Eq |
| 1830 → 2060 | `STRING(zsZ,2,4)` | x value | ne_Fx |
| 1831 → 2061 | `STRING(zsX,2,2)` | x value | ne_Fx |
| 1831 → 2061 | `STRING(zsM,2,2)` | parameter | ne_Fx |
| 1832 → 2062 | `STRING(zsS,2,2)` | parameter | ne_PStr |
| 1848 → 2078 | `STRING(zsZ,2,4)` | x value | ne_Fx |
| 1848 → 2078 | `STRING(zsM,2,4)` | parameter | ne_Fx |
| 1849 → 2079 | `STRING(zsS,2,4)` | parameter | ne_PStr, ne_Eq |
| 1850 → 2080 | `STRING(zsX,2,4)` | x value | ne_Fx |
| 1851 → 2081 | `STRING(zsM,2,2)` | parameter | ne_Fx |
| 1851 → 2081 | `STRING(zsZ,2,2)` | x value | ne_Fx |
| 1852 → 2082 | `STRING(zsS,2,2)` | parameter | ne_PStr |
| 1868 → 2098 | `STRING(zsX,2,4)` | x value | ne_Fx |
| 1868 → 2098 | `STRING(zsZ,2,4)` | x value | ne_Fx |
| 1869 → 2099 | `STRING(zsS,2,4)` | parameter | ne_PStr, ne_Eq |
| 1870 → 2100 | `STRING(zsM,2,4)` | parameter | ne_Fx |
| 1871 → 2101 | `STRING(zsX,2,2)` | x value | ne_Fx |
| 1871 → 2101 | `STRING(zsZ,2,2)` | x value | ne_Fx |
| 1872 → 2102 | `STRING(zsS,2,2)` | parameter | ne_PStr |
| 1887 → 2118 | `STRING(zsS,2,4)` | parameter | ne_Fx |
| 1893 → 2124 | `STRING(zsX,2,4)` | x value | ne_Fx |
| 1893 → 2124 | `STRING(zsM,2,4)` | parameter | ne_Fx |
| 1894 → 2125 | `STRING(zsZ,2,4)` | x value | ne_Fx |
| 1895 → 2126 | `STRING(zsS,2,4)` | parameter | ne_PStr, ne_Eq |
| 1896 → 2127 | `STRING(zsX,2,2)` | x value | ne_Fx |
| 1896 → 2127 | `STRING(zsM,2,2)` | parameter | ne_Fx |
| 1897 → 2128 | `STRING(zsZ,2,2)` | x value | ne_Fx |
| 1951 → 2195 | `STRING(c2A,2,4)` | probability | ne_PStr, ne_Eq |
| 1951 → 2195 | `STRING(c2X,2,4)` | x value | ne_Fx |
| 1952 → 2196 | `STRING(NE_CFG(3),2,4)` | parameter | ne_Fx |
| 1953 → 2197 | `STRING((NE_CFG(3) - NE_MU) / NE_SG,2,3)` | parameter | ne_Fx |
| 1954 → 2198 | `STRING(c2Pw,2,4)` | probability | ne_PStr, ne_Eq |
| 1955 → 2199 | `STRING(1 - c2Pw,2,4)` | probability | ne_PStr, ne_Eq |
| 2271 → 2522 | `STRING(zdN,2,0)` | count | ne_Fx |
| 2272 → 2523 | `STRING(zdXB,2,4)` | parameter | ne_Fx |
| 2272 → 2523 | `STRING(zdS,2,4)` | parameter | ne_PStr, ne_Eq |
| 2419 → 2672 | `STRING(NE_MU,2,2)` | parameter | ne_Fx |
| 2419 → 2672 | `STRING(NE_SG,2,2)` | parameter | ne_PStr |
| 2420 → 2673 | `STRING(NE_WLO,2,1)` | x value | ne_Fx |
| 2420 → 2673 | `STRING(NE_WHI,2,1)` | x value | ne_Fx |
| 2422 → 2675 | `STRING(NBINS,2,0)` | count | ne_Fx |
| 2423 → 2676 | `STRING(NE_HN,2,0)` | count | ne_Fx |
| 2602 → 2857 | `STRING(NE_MU,2,2)` | parameter | ne_Fx |
| 2602 → 2857 | `STRING(NE_SG,2,2)` | parameter | ne_PStr |
| 2631 → 2888 | `STRING(NE_Z,2,4)` | x value | ne_Fx |
| 2631 → 2888 | `STRING(NE_X,2,4)` | x value | ne_Fx |
| 2632 → 2889 | `STRING(NE_P,2,4)` | probability | ne_PStr, ne_Eq |
| 2675 → 2934 | `STRING(tgP, 2, 4)` | probability | ne_PStr |
| 2822 → 3081 | `STRING(ndYV, 2, ndYDec)` | axis | ne_Fx |
| 2902 → 3163 | `STRING(ndXV, 2, ndDec)` | axis | ne_Fx |
| 2925 → 3186 | `STRING(ndK, 2, 0)` | axis | ne_Fx |
| 3192 → 3459 | `STRING(ndMU, 2, 2)` | parameter | ne_Fx |
| 3193 → 3460 | `STRING(ndSG, 2, 2)` | parameter | ne_PStr, ne_Eq |
| 3200 → 3467 | `STRING(ndMU2,2,2)` | parameter | ne_Fx |
| 3203 → 3470 | `STRING((ndMU2-ndMU)/ndSG,2,2)` | parameter | ne_Fx |
| 3208 → 3475 | `STRING(ndN,2,0)` | count | ne_Fx |
| 3210 → 3477 | `STRING(ndN,2,0)` | count | ne_Fx |
| 3222 → 3489 | `STRING(NE_HXB,2,2)` | parameter | ne_Fx |
| 3225 → 3492 | `STRING(NE_HS,2,2)` | parameter | ne_PStr, ne_Eq |
| 3237 → 3504 | `STRING(ndMU-ndSG,2,2)` | x value | ne_Fx |
| 3238 → 3505 | `STRING(ndMU+ndSG,2,2)` | x value | ne_Fx |
| 3239 → 3506 | `STRING(ndMU-2*ndSG,2,2)` | x value | ne_Fx |
| 3240 → 3507 | `STRING(ndMU+2*ndSG,2,2)` | x value | ne_Fx |
| 3241 → 3508 | `STRING(ndMU-3*ndSG,2,2)` | x value | ne_Fx |
| 3242 → 3509 | `STRING(ndMU+3*ndSG,2,2)` | x value | ne_Fx |
| 3255 → 3525 | `STRING(ndLoB,2,2)` | x value | ne_Fx |
| 3256 → 3526 | `STRING((ndLoB-ndMU)/ndSG,2,2)` | x value | ne_Fx |
| 3269 → 3539 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3278 → 3548 | `STRING(ndYW,2,ndHD)` | density | ne_PStr |
| 3289 → 3559 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3296 → 3573 | `STRING(ndLoB,2,2)` | x value | ne_Fx |
| 3296 → 3573 | `STRING(ndHiB,2,2)` | x value | ne_Fx |
| 3304 → 3581 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3312 → 3589 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3315 → 3592 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3318 → 3595 | `STRING(ndPV,2,4)` | probability | ne_PStr, ne_Eq |
| 3325 → 3604 | `STRING(ndQ,2,4)` | probability | ne_PStr, ne_Eq |
| 3371 → 3659 | `STRING(ndB,2,0)` | count | ne_Fx |
| 3371 → 3659 | `STRING(ndBins(ndB),2,0)` | count | ne_Fx |
| 3372 → 3660 | `STRING(ndExp,2,1)` | count | ne_PStr |
| 3374 → 3662 | `STRING(ndXV,2,2)` | x value | ne_Fx |
| 3375 → 3663 | `STRING(ndXV + NE_HW,2,2)` | x value | ne_Fx |
| 3375 → 3663 | `STRING(ndQ,2,4)` | probability | ne_PStr, ne_Eq |

## Verification

`verify_NormExplorer_beta42a.py` was built from `verify_NormExplorer.py` (beta 42), and every one of its checks is kept. It runs on beta 42a, and runs beta 42 beside it wherever a comparison shows a fix. The output is in `verify_NormExplorer_beta42a_output.txt`: **322 checks, 0 failures**.

- **Parts A-B (kept):** beta 42's 135 checks (129 `check`/`check_true` calls and 6 S-curve cache lines, all now counted). They are the formulas against SciPy and the kit-interpreter runs of every module, now on beta 42a, and all pass. Their mini-harness prints plain fixed decimals, so it cannot see the scientific form. Its builtin patches are undone before Part C. No old expected value had to change.
- **Part C (the review's regression tests):** each script is run in a subprocess with its `SRC` pointed at each file.
  - `check_NormExplorer.py`: beta 42 fails exactly B1, B2 and B3, the review's three scientific-form asserts (62 checks, 3 failures); beta 42a passes 62 of 62.
  - `check_NormExplorer_python.py` (the `#PYTHON` block in CPython): 6 runs and 0 failures on beta 42a, with output identical to beta 42's.
- **Part D1 (D-NE-1):**
  - The headline: beta 42 prints `P(X > x) = 4.8213ᴇ−8` and beta 42a prints `P(X > x) < 0.0001`.
  - 31 unit checks of the three helpers.
  - The review's reproduction table, row by row, on both files.
  - A sweep of 244 runs over every module at ordinary and extreme inputs: x from −40σ to +40σ on three distributions, the four area types, all five inverse items, the z-solver, the power picture, the window and diagnostics pages, D2, the Explorer, the bars, a full `NormExp` session, the animation and help. Beta 42a showed 17,645 texts; none has a small-capital E, `= <` or a negative zero. The same runs on beta 42 printed 1,422 scientific strings.
  - Every probability on the Probability-from-x panels, and the final readout of each run, is within half a last digit of SciPy, and reads `< 0.0001` exactly when it is positive and rounds to zero. `NE_P` equals SciPy to 1E-12.
  - "Between" 8..10σ and 9..12σ to the right of μ is right too (beta 42: 0.0000).
- **Part D2 (D-NE-2):** the Prime's 12 significant digits are modelled on the statistics built-ins, using `check_StatDist.py`'s `twelve_digits`.
  - `NE_P` for the right tail at z = 5.33, 6, 7, 8, 9 and 12 equals SciPy's sf to 12 digits. Beta 42's is exactly 0 from z = 8.
  - Also checked: both complements, outside ±8σ, power and β far out, and the readouts and riding tags.
- **Part D6 ("between", mirrored, 12-digit model):**
  - between 9..12σ and 8..10σ: `NE_P` equals SciPy, and the panel and view read `< 0.0001`; beta 42 had `NE_P` 0 and `= 0.0000`;
  - between 2..3σ, −3..−2σ and −1..9σ: unchanged from beta 42 to the last digit;
  - the outside panel's "Between area", the result-view readout with its riding tag, and the Explorer's "area between": beta 42a right, beta 42 `0.0000`;
  - a bar 9σ or more above the curve: `< 0.1 expected`, `p < 0.0001` (beta 42: `0.0 expected`, `p = 0.0000`).
- **Part D7 (right-tail quantiles, 12-digit model).** The model also holds `NORMALD_ICDF`'s argument to 12 digits, as the Prime holds every real.
  - At α = 1E-13 (right tail, two tails, power picture), beta 42 stops at `NORMALD_ICDF(…, 1)`; beta 42a's z* equals SciPy's.
  - At C = 0.999999999999 (and 99.9999999999 as a percent), beta 42 is wrong either way: on the Prime 1 + C rounds to 2 and it stops; the harness, which adds in doubles, gives z* = 7.0345. Beta 42a gives 7.1305, which is SciPy's.
  - At α = 0.05 and C = 0.95, z* is beta 42's to 1E-9.
  - Every form was run at its edges (1E-300, 1E-13, 0.5, 0.999999999999, and C = 1 and 99.9999999999): 21 runs, no stop, every `NORMALD_ICDF` argument strictly inside 0..1, and no E, `= <` or −0 on screen.
  - The source holds exactly the six `NORMALD_ICDF` calls listed under change 8, and none forms 1 − p or (1 + C)/2.
- **Part D3:** the CHOOSE idiom is checked in the source (8 CHOOSE calls, none assigned, every index set to 0 before it and tested alone after it). Esc in each of the 7 menus, and Simulate then Esc, shows the menu and then nothing, as in beta 42.
- **Part D4:** C = 1 gives a 1 % interval (NE_P 0.01, upper end μ + Φ⁻¹(0.505)σ). C = 100 is refused. C = 95, 0.95, 99.9 and 0.5 give the same results as beta 42.
- **Part D5:** a σ drag from 15 to 2, then → (μ 100.5; beta 42: 105), → ↑ (σ 2.2; beta 42: 4), and ← ↓ (99.5 and 1.8; beta 42: 95 and 2).
- **Part E, the source:**
  - one `STRING` is left, inside `ne_Fx`, and 134 `ne_Fx`/`ne_PStr` calls replace beta 42's 134;
  - exactly six `NORMALD_ICDF` calls, each taking an area its form keeps inside 0..1;
  - the banners, the map's line count, the tested-on lines, the dated paragraph and the disclaimer are as described;
  - each helper is forward-declared and defined before its first use, and no new name matches a built-in, case ignored;
  - every LOCAL line holds 6 names or fewer, and no `//` comment sits inside an open bracket;
  - no `1 − CDF` is left, the INSTRING count is unchanged (0), and the new `LEFT` is guarded by `DIM`;
  - the ppl_check_v4 tally equals beta 42's;
  - lint_ppl reports 67 problems, against beta 42's 75: the 7 CHOOSE-capture lines and the `STRING(NORMALD(..),2,4)` miscount are gone, and nothing is new.
- **Part F, the routine diff:**
  - Changed (12): `ne_Explorer` (D-NE-5), `ne_SetWin`, `ne_ProbCalc`, `ne_InvCalc`, `ne_ZSolve`, `ne_Compare2`, `ne_Histo`, `ne_ZtoD2`, `ne_DiagPage`, `NormExp`, `ne_Tag` and `ne_NormDraw`. The two tail items touch only routines already on this list: `ne_ProbCalc`, `ne_InvCalc`, `ne_Compare2` and `ne_NormDraw`.
  - Added (4): `ne_Fx`, `ne_PStr`, `ne_Eq` and `ne_Btw`.
  - Byte-identical (23), including `#PYTHON SAMPBINSPY`.
  - Outside the routines, only the header, the disclaimer, the map, the beta 42a paragraph, the forward declarations and the helpers' comments changed.
- **h.sci_strings:** every ppl_run_v3e run of beta 42a, in 31 scenario groups, left it **empty**. The listing at the end of the output shows beta 42's entries beside them.

Run time is about 7 minutes, most of it the sweep and the review's check script.

## Gate

- `python3 ppl_gate_v1b.py NormExplorer_beta42a.txt _old/NormExplorer_beta42.txt` in `gate_f19` gives **RESULT: PASS**.
  - hp-prime-kit lint: 0 errors.
  - ppl_check_v4: 5 E5 and 6 W3, the same as beta 42; no hard errors, E12 included.
  - lint_ppl: 67 problems (beta 42: 75). What remains is the `#PYTHON` block's `#END`, the multi-line `IF INPUT(...) == 0` miscount and the G0 "not a GROB" noise, all as in beta 42.
  - Full parse: it stops at `√` (801; beta 42 at 643), the tool's limit.
  - fleet_names_v2: 25 files, 1,293 routine names, 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.
- `bash check.sh NormExplorer_beta42a.txt out/NormExplorer_beta42.txt`: kit lint 0 errors, no hard errors, and the parse fails on the same `√` as the old file.

## Device checklist (emulator first, then G2 and G1)

1. **Paste and check.** Open beta 42 in the Kit and paste over it, then Program Catalog → Check. If it stops, note the line: the forward declarations (476-479), the helpers (683-735), or a minus before `NORMALD_ICDF` (1866, 1920, 1954, 2181).
2. **Right tail at x = 180** (the review's §5 test). Menu 1: N(100, 15). Menu 3: P(X > x), x = 180.
   - The panel reads `P(X > x) < 0.0001` and `Complement: P(X < x) = 1.0000`.
   - The view reads `P(X > x₀) < 0.0001`, and no `ᴇ` shows anywhere.
   - Quit. In Home, `NE_P` shows 4.82…E-8.
3. **The far tail in Home.** Type `NORMALD_CDF(0,1,-8)` in Home; it should show 6.22096057427E-16 (if it shows 0, D-NE-2 is harmless but gains nothing). Then run menu 3, P(X > x), at x = 220 on N(100, 15).
   - The panel reads `P(X > x) < 0.0001`.
   - After Quit, Home's history line reads `NormExp: z = 8.0000, x = 220.0000, p < 0.0001`, and `NE_P` = 6.22…E-16 (beta 42: 0).
4. **Menu 4.**
   - Percentile with area `1E-9`, pasted: `area left < 0.0001` and `< 0.1% of the distribution falls below x`.
   - Central with C = `1`: `Central 1.0% interval`.
   - C = `100`: refused.
   - C = `0.9999`: `each tail 0.01%`, where the PC printed `< 0.01%`; either is right.
5. **Explorer (menu 2) on N(0, 1).** Drag x₀ slowly to the left edge: `area to the left < 0.0001` and `height < 0.000001 (density,`, with no `ᴇ` at any point of the drag.
6. **D-NE-5.** Menu 1: N(100, 15). Menu 2: press the small square on the right shoulder and drag it inward until σ stops shrinking (σ = 2), then lift. → gives μ = 100.5 (beta 42: 105); ↑ gives σ = 2.2.
7. **D-NE-3.** Open menus 9, 3, 4, 5, 7 and 6, then 6 → Simulate, and press Esc in each. Each goes back to the main menu with nothing else happening.
8. **The power picture far out.** Menu 7 item 1: μ₂ = −8 on N(0, 1). Then item 3, α 0.05. The panel and the plot both read `power < 0.0001`.
9. **"Between" far right (change 7).** Menu 3, between, a = 235 and b = 280 on N(100, 15).
   - The panel and the view read `P(a < X < b) < 0.0001` (beta 42: `= 0.0000`).
   - After Quit, `NE_P` is about 1.13E-19.
10. **Tiny α (change 8).**
    - Menu 4, right-tail critical value, α = `1E-13`, pasted: z* = 7.3488, with no error.
    - Central interval with C = `0.999999999999`: z* = 7.1305.
    - Menu 7 item 3 with α = `1E-13`: x* = μ + 7.3488σ.
    - Beta 42 should stop on each of these; if the Prime instead returns ∞ there, note it (review §5).
11. Glance at the header: the DISCLAIMER sits under the terms.

## Unresolved

- **D15 (open):** tiny areas print `< 0.0001`, the honest minimum the brief asks for. If Roger chooses `0.0000`, it is one line in `ne_PStr` (return `ne_Fx(psV, psD)` only). The same rule covers σ, s, the densities, widths and expected counts (`σ < 0.01`, `< 0.1 expected`).
- **The two tail items found while verifying** ("between" far right, and quantiles of 1 − α) are fixed in this version, changes 7 and 8, at the coordinator's request.
- **The bound step** is fitted to σ at entry and refits neither after a σ drag nor on Centre.
- **Signed values** (z, x, d, μ) round as usual, so z for an x within 0.00005σ of μ prints `0.0000`. The brief's "< 0.001 style" is applied to quantities that cannot be negative.
- **The guide** `normexplorer-guide_beta42.md` is not updated. It does not mention `< 0.0001`, a typed C of 1, or the step refit after a σ drag.
- **Still pending from beta 42:** the five `√`, `K` as the MAKELIST counter, and the program's own hex palette.

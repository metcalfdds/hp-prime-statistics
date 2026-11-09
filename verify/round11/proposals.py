# Help-page plain-language proposals (Roger, 9 Nov 2026, 07:18: "Ok start with the help pages...").  For his approval before any
# program changes.  Each entry: (program, page, old wording as it reads on the page, new wording, why).  Old wording is quoted from
# helppages.json (the book's dump of every page, 7 Nov 2026); line breaks are the calculator's own and are re-made by the program.
P = []
def add(prog, page, old, new, why): P.append((prog, page, old, new, why))

# ---------------------------------------------------------------- AgreeLab
add('AgreeLab', 2, "'better than chance' is a low bar: raters who agree on 1 in 3 can beat it easily.",
    "'better than chance' is easy to reach: raters who agree on only 1 item in 3 can reach it.", 'idiom ("a low bar")')
add('AgreeLab', 2, "Read the CI: how much agreement, how sure.",
    "The CI says how much agreement there is, and how precisely it is known.", 'telegraphic')
add('AgreeLab', 6, "(2,1) same raters, a sample: ABSOLUTE agreement, rater offsets count;",
    "(2,1) same raters, a sample: ABSOLUTE agreement; a rater who scores every target higher lowers it;", '"rater offsets count" unexplained')
add('AgreeLab', 6, "(.,k): the reliability of the MEAN of k.",
    "(1,k), (2,k), (3,k): the reliability of the MEAN of the k raters.", '"(.,k)" is notation, not words')
add('AgreeLab', 7, "bias = \nd\n;  [as dumped: three lines]",
    "bias = d̄, the mean difference;", 'says what d̄ is (the book also prints this line as three lines today, a fault of the harness\'s copy that is fixed in the book either way)')
add('AgreeLab', 7, "Trend: regress d on the mean; a slope says the disagreement grows with the size.",
    "Trend: regress d on the mean; a slope means the two methods differ more for larger (or smaller) values.", 'vague ("the size")')

# ---------------------------------------------------------------- AnovaLab
add('AnovaLab', 2, "Levene's test (Brown-Forsythe form) runs the one-way F on |value - group median|: robust.",
    "Levene's test (Brown-Forsythe form) runs the one-way F on |value - group median|; non-normal data affect it little.", '"robust" unexplained')
add('AnovaLab', 2, "Insect sprays: s runs from 1.7 to 6.2, Levene flags it; compare the ordinary F with Welch's.",
    "In the insect-spray preset, s runs from 1.7 to 6.2 and Levene's test flags it; compare the ordinary F with Welch's.", 'telegraphic')
add('AnovaLab', 2, "A check that is not significant is not proof of equal spreads: small groups miss a lot.",
    "A check that is not significant is not proof of equal spreads: with small groups the checks often miss real differences.", '"miss a lot" vague')
add('AnovaLab', 3, "Many t-tests inflate the chance of a false alarm; these keep it at α for the family:",
    "Many t-tests raise the chance of at least one false alarm; these keep that chance at α for the whole set (the family):", '"inflate", "the family" unexplained')
add('AnovaLab', 3, "(asks first: slow)", "(it asks before it runs, since it is slow)", 'telegraphic')
add('AnovaLab', 3, "Holm: step-down Bonferroni, never less power.", "Holm: Bonferroni done in steps; never less power than Bonferroni.", '"step-down" unexplained; "less power" than what')
add('AnovaLab', 4, "Swap turns the plot.", "Swap exchanges the two factors in the plot.", '"turns" unclear')
add('AnovaLab', 4, "Mock jury: unattractive swindlers: 7.0 years; other cells 3.5 to 4.8: striking, yet the interaction's p is 0.13 (cells of 17 to 21).",
    "Mock-jury preset: unattractive swindlers got 7.0 years on average, the other cells 3.5 to 4.8; striking, yet the interaction's p is 0.13 (17 to 21 jurors a cell).", 'telegraphic')
add('AnovaLab', 7, "Soft keys: More turns to more keys (one-way).", "Soft keys: More shows the next set of soft keys (one-way).", '"turns to" unclear')

# ---------------------------------------------------------------- BayesTree
add('BayesTree', 1, "Leaf bars: share of N (a log stub below 1 %).",
    "Leaf bars: each leaf's share of N (a share below 1 % gets a short bar on a log scale).", '"a log stub" unexplained')
add('BayesTree', 1, "Soft keys: More (slot 6) turns to the next page:", "Soft keys: More (the 6th key) shows the next set of keys:", '"slot 6", "page" (it is a set of keys)')
add('BayesTree', 2, "the root is the T+ people of test 1 (gray).", "the tree now starts from the people who were positive on test 1 (gray).", '"the root" unexplained')
add('BayesTree', 4, "The CAS is asked only when you stop -- after a key, a lift or a view, never during a drag.",
    "The CAS is asked only when you stop: after a key press, a finger lift, or a change of view; never during a drag.", '"a lift" unexplained')

# ---------------------------------------------------------------- BiNorm3D
add('BiNorm3D', 1, "ρ = 0: a round bell.  X says nothing about Y.", "ρ = 0: a round bell.  Knowing X tells you nothing about Y.", 'personification')
add('BiNorm3D', 5, "Drag: sideways turns, downward raises the eye.", "Drag sideways to turn the surface; drag down to look at it from higher up.", '"raises the eye"')
add('BiNorm3D', 5, "Arrows: Left, Right turn; Up, Down raise and lower the eye; 10° a step.",
    "Arrows: Left and Right turn it; Up and Down look from higher or lower; 10° a press.", '"raise and lower the eye"')

# ---------------------------------------------------------------- BurrLab
add('BurrLab', 1, "with a heavy enough tail the sample mean never settles (menu 4).",
    "with a heavy enough tail the sample mean never settles down to one value (menu 4).", '"settles" incomplete')
add('BurrLab', 1, "The window freezes while a finger is down and refits on the lift.",
    "The plot holds still while your finger is on the screen and is fitted again when you lift it.", '"freezes", "refits on the lift"')
add('BurrLab', 2, "Tap the map to set (C, K); its colors are the moment cases.",
    "Tap the map to set (C, K); its colors show whether the mean and the variance exist there.", '"the moment cases" unexplained')
add('BurrLab', 2, "A fit that runs to the Weibull or Pareto limit is named as such.",
    "If the best fit is at the Weibull or Pareto limit, the fit is named that.", 'telegraphic')
add('BurrLab', 2, "Anderson-Darling (a statistic, honestly without a p).",
    "Anderson-Darling (the statistic only, with no p-value).", '"honestly" leaves the reason unsaid')
add('BurrLab', 4, "Python only: no fallback; a bridge failure shows a message,",
    "Python only: no fallback; if the Python engine fails, a message says so,", '"a bridge failure" unexplained')

# ---------------------------------------------------------------- CICatcher
add('CICatcher', 1, "Blue lines caught it, red lines missed it.",
    "A blue line caught it (the interval contains it); a red line missed it.", 'say once what "caught" means')
add('CICatcher', 1, "The 95 % is the METHOD'S long-run catch rate, not a property of any one interval.",
    "The 95 % is the share of intervals the METHOD catches in the long run, not a property of any one interval.", '"catch rate"')
add('CICatcher', 1, "Keep adding samples: the 'all' rate in the header settles near the target.",
    "Keep adding samples: the 'all' rate at the top of the screen settles near the confidence level.", '"the header", "the target"')
add('CICatcher', 2, "99 % catches more but says less.", "99 % catches more, but its longer lines give a less precise answer.", '"says less"')
add('CICatcher', 2, "and t* is bigger than z* to pay for it:", "so t's critical value is bigger than z's to make up for that:", '"t*", "z*", "pay for it"')
add('CICatcher', 3, "Wilson (score) takes its SE from the p being tested, not from p̂:",
    "Wilson (score) takes its SE from each possible p, not from p̂, and keeps every p within z SEs of p̂:", 'the same unclear sentence as the book had: there is no test in an interval')
add('CICatcher', 3, "Wald wants n × p and n × (1 - p) of 10 or more;", "Wald needs n × p and n × (1 - p) to be 10 or more;", 'personification')
add('CICatcher', 4, "it keeps every p under which your count is in neither tail of Binomial(n, p) holding α/2.",
    "it keeps every p for which your count is not in either α/2 tail of Binomial(n, p).", 'hard to parse')
add('CICatcher', 4, "The price: longer lines.", "The cost: longer lines (wider intervals).", '"price"')

# ---------------------------------------------------------------- CentralLimit
add('CentralLimit', 1, "Bottom: one bar-count per sample mean x̄.",
    "Bottom: a histogram of the sample means, x̄.", '"bar-count" unexplained')
add('CentralLimit', 1, "Both panels share ONE x-axis: means bunch up.",
    "Both panels share ONE x-axis, so you can see the means bunch up more tightly than the population.", 'telegraphic')
add('CentralLimit', 1, "σ/SD: how many times narrower the means are; close to √n, so every n offered is a square.",
    "σ/SD: how many times narrower the spread of the means is; it is close to √n, which is why every n offered is a square number.", 'telegraphic')
add('CentralLimit', 2, "their mean falls into the pile.", "their mean is added to the histogram.", '"the pile"')
add('CentralLimit', 2, "n− n+ (or − +): n = 1, 4, 16, 64, 100; draws.", "n− n+ (or − +): change n (1, 4, 16, 64, 100) and draw new samples.", 'telegraphic')
add('CentralLimit', 2, "the curve moves first, lift to draw.", "the curve changes as you drag; lift your finger to draw the samples.", 'telegraphic')
add('CentralLimit', 2, "n = 100 is item (A); big n draws fewer samples.", "In the menu, n = 100 is item (A); a large n draws fewer samples.", 'item of what')

# ---------------------------------------------------------------- ChiTable
add('ChiTable', 1, "a big χ² means a big surprise.", "a big χ² means the counts are far from what independence predicts.", '"a big surprise"')
add('ChiTable', 3, "N / 10 (V stays, p moves)", "N / 10 (Cramér's V stays the same; p changes)", 'telegraphic')
add('ChiTable', 3, "Mosaic: Morph (or +) melts O into E: H₀ itself.",
    "Mosaic: Morph (or +) changes the observed counts, step by step, into the expected counts: what the table would look like if H₀ were true.", '"melts", "H₀ itself"')
add('ChiTable', 3, "near .001 .005 .01 .02 .05 .10 .20 it snaps to them; ← → step that ladder;",
    "near .001 .005 .01 .02 .05 .10 .20 it jumps to the nearest one; ← → step through those values;", '"snaps", "ladder"')
add('ChiTable', 5, "Add the tables no likelier than yours.", "p adds up the chances of every table no more likely than yours.", 'telegraphic')

# ---------------------------------------------------------------- DNAMixLR
add('DNAMixLR', 1, "P(E|H): the chance 2x random alleles do that.", "P(E|H): the chance that the x unknowns' 2x alleles (two each, drawn at random) do exactly that.", 'telegraphic')
add('DNAMixLR', 1, "LR = P(E|Hp) / P(E|Hd); loci multiply.", "LR = P(E|Hp) / P(E|Hd); the loci's LRs multiply.", 'telegraphic')
add('DNAMixLR', 2, "ALL typed people condition it, contributors or not (Curran et al. 1999).",
    "Every typed person's alleles count in it, contributor or not (Curran et al. 1999).", '"condition it" unexplained')
add('DNAMixLR', 2, "1e3-1e4 strong, 1e4-1e6 very strong, above 1e6 extremely so.",
    "1,000-10,000 strong, 10,000-1,000,000 very strong, above 1,000,000 extremely strong.", 'e-notation; commas in big numbers (house style)')
add('DNAMixLR', 3, "THETA PLOT: drag across it (or Left/Right); LR and the ladder follow.  Ent adopts θ.",
    "THETA PLOT: drag across it (or Left/Right); the LR and the Ladder view change with θ.  Ent keeps that θ.", '"follow", "adopts"')
add('DNAMixLR', 3, "LADDER: the LR builds locus by locus.", "LADDER: the LR multiplied up one locus at a time.", '"builds"')
add('DNAMixLR', 3, "see Prosecutor's fallacy (8).", "see Prosecutor's fallacy (menu item 8).", '"(8)" of what')
add('DNAMixLR', 4, "how far θ must go before the words change.", "how far θ must rise before the LR moves into the next ENFSI band.", '"the words change"')

# ---------------------------------------------------------------- DataLoad
add('DataLoad', 1, "the lists the fleet's programs read:", "the lists our programs read:", '"the fleet" is our working word, not the book\'s')

# ---------------------------------------------------------------- EpiStats
add('EpiStats', 1, "EP_* results.  Touch: Help 9-D; exact: E, F.",
    "Results are kept in Home as EP_ variables (help page 8).  Touch and keys: help pages 9 to 13; exact answers: pages 14 and 15.", 'cryptic')
add('EpiStats', 5, "Exact (Clopper-Pearson) beside it: Help E.", "Exact (Clopper-Pearson) beside it: help page 14.", '"Help E"')
add('EpiStats', 5, "Its SE: Help F.", "Where its SE comes from: help page 15.", '"Help F"')
add('EpiStats', 6, "Small p: report them separately.", "A small p means the strata's ORs differ: report them separately.", 'telegraphic')
add('EpiStats', 6, "tap again = back.", "tap it again to put it back.", 'telegraphic')
add('EpiStats', 11, "+/- = page.", "+/- turn the page.", 'telegraphic')
add('EpiStats', 13, "Tap a stratum (Up = 1, Down = 2): drop/restore.", "Tap a stratum (or press Up for stratum 1, Down for stratum 2) to drop it from the pool or put it back.", 'telegraphic')
add('EpiStats', 14, "every p under which your count is in neither 2.5 % tail of Binomial(n, p).",
    "every p for which your count is not in either 2.5 % tail of Binomial(n, p).", 'hard to parse (same as CICatcher)')
add('EpiStats', 14, "mid-P counts half of P(X = k): nearer 95 %.", "The mid-P interval counts only half of P(X = k), so its coverage is nearer 95 %.", 'telegraphic')

# ---------------------------------------------------------------- ErrorRate
add('ErrorRate', 2, "Green band: rates the record allows.", "Green band: true error rates that fit this record.", '"allows"')
add('ErrorRate', 2, "Log y (page 2): the k = 0 curve is a line.", "Log y (soft key, page 2): on a log scale the k = 0 curve is a straight line.", 'telegraphic')
add('ErrorRate', 5, "Each run jumps from one error to the next: the clean run before an error has a geometric length, ln(U)/ln(1 - p).",
    "To save time, each simulated examiner skips from one error to the next: the number of clean tests before an error is geometric, drawn as ln(U)/ln(1 - p).", 'hard to follow')
add('ErrorRate', 6, "A cold hit from a big database needs more support than the RMP alone.",
    "A cold hit (a match found only by searching a database) from a big database needs more support than the RMP alone.", '"cold hit" unexplained')
add('ErrorRate', 7, "ErrorRate help 7/9: Honest caveats", "ErrorRate help 7/9: Cautions", '"honest" implies the other pages are not')
add('ErrorRate', 7, "Easy or similar items make it too optimistic.", "Easy or similar items make the bound too low (too optimistic).", '"it"')
add('ErrorRate', 8, "More = pages.", "More shows the other set of soft keys.", 'telegraphic')
add('ErrorRate', 9, "MicroPython simulates 10,000 programs;", "MicroPython simulates 10,000 examiners;", 'an error: it simulates examiners, not programs')
add('ErrorRate', 9, "Eng (page 2) checks the CAS and Python live and says which ran last.",
    "Eng (page 2) checks that the CAS and Python are working, and says which one ran last.", '"live"')

# ---------------------------------------------------------------- ExhibitLab
add('ExhibitLab', 1, "a random sample of this size would come out this clean (this few negatives or fewer) at most 5% of the time: the METHOD rarely backs a false claim.",
    "a random sample of this size would show this few negatives (or fewer) at most 5% of the time: the METHOD rarely supports a false claim.", '"this clean", "backs"')
add('ExhibitLab', 2, "Suppose the claim is just false (K₀ drug units);", "Suppose the claim is false by the smallest margin (K₀ drug units);", '"just false"')
add('ExhibitLab', 2, "Jeffreys Beta(0.5, 0.5) leans to all or none.", "Jeffreys Beta(0.5, 0.5) gives more weight to proportions near 0 and 1.", '"leans to all or none"')
add('ExhibitLab', 3, "no negatives: least n 8 at N = 10,", "no negatives: the smallest n is 8 at N = 10,", 'telegraphic')
add('ExhibitLab', 3, "the magenta staircase settles onto the blue binomial.", "the magenta steps (the hypergeometric) come to lie on the blue binomial curve.", 'figurative')
add('ExhibitLab', 7, "Up/Down = neg;", "Up/Down = negatives allowed;", 'abbreviation')

# ---------------------------------------------------------------- book-only (the dump, not the program)
add('NormExplorer', 2, "[the book prints the soft-key table as alternating lines: 'Bands' / '68-95-99.7 bands on or off (+)' / 'Ref' / ...]",
    "(the book's copy: print each key with its meaning on one line, 'Bands: 68-95-99.7 bands on or off (+)', as the calculator shows them side by side)", 'the book prints each key on one line and its meaning on the next; the calculator shows them side by side, as on both sides here')

# ---------------------------------------------------------------- FitCheck
add('FitCheck', 3, "The curve is only a fair guide when the E are not too small:",
    "The χ² curve gives a trustworthy p only when the E are not too small:", '"a fair guide"')
add('FitCheck', 5, "a normal sample hugs the line x̄ + s z.", "a normal sample lies close to the line x̄ + s z.", '"hugs"')
add('FitCheck', 5, "(D'Agostino & Stephens 1986): weights the tails.", "(D'Agostino & Stephens 1986): gives extra weight to the tails.", 'telegraphic')
add('FitCheck', 6, "so a p of 10^-145 (Castaneda) is still printed as a number.  The plot puts x on a scale of SDs from E (the Castaneda reasoning).",
    "so a p of 10^-145 (the Castaneda jury preset) is still printed as a number.  The plot shows how many SDs x is from E, the reasoning the Supreme Court used in Castaneda v. Partida (1977).", '"Castaneda" unexplained')

# ---------------------------------------------------------------- GaltonBoard
add('GaltonBoard', 1, "Sweep rows 3 to 12 (up key).", "Try rows 3 to 12 (the Up key).", '"sweep"')
add('GaltonBoard', 2, "×10 = ten in the air;", "×10 = ten balls at once;", '"in the air"')
add('GaltonBoard', 2, "Drag sideways over the pegs: p follows your finger; lift = a new board (the counts clear).",
    "Drag sideways over the pegs: p changes with your finger; lifting it starts a new board (the counts are cleared).", 'telegraphic')
add('GaltonBoard', 2, "Keys: - = 1, + = 100, 0 = pour,", "Keys: - = one ball, + = 100 balls, 0 = pour,", '"- = 1"')
add('GaltonBoard', 3, "the binomial bars close in on the Poisson.", "the binomial bars come closer and closer to the Poisson.", '"close in on"')

# ---------------------------------------------------------------- Norm3
add('Norm3', 1, "Lift: x₀ snaps to a round value.", "When you lift your finger, x₀ moves to the nearest round value.", '"snaps"')
add('Norm3', 1, "p is that height and x₀ its quantile. Drag up the curve to 0.900.",
    "p is that height, and x₀ is the value with area p to its left. Drag up the curve to 0.900, for example.", '"its quantile" unexplained')

# ---------------------------------------------------------------- NormExplorer
add('NormExplorer', 2, "EXPLORER SOFT KEYS  (More turns the page)", "EXPLORER SOFT KEYS  (More shows the second set)", '"turns the page"')
add('NormExplorer', 2, "Tap the chosen key again for the usual:", "Tap the chosen key again to go back to the usual keys:", 'telegraphic')
add('NormExplorer', 2, "The window is held while you explore.", "The plot's window stays fixed while you explore.", '"held"')
add('NormExplorer', 3, "Lifting snaps μ and σ.", "When you lift your finger, μ and σ move to round values.", '"snaps"')
add('NormExplorer', 3, "The area rides the shaded region;", "The area's value is printed on the shaded region;", '"rides"')

# ---------------------------------------------------------------- PowerViz
add('PowerViz', 1, "α− / α+ = α ladder .001 .005 .01 .02 .05 .10 .20", "α− / α+ = step α through .001 .005 .01 .02 .05 .10 .20", '"the α ladder" never explained')
add('PowerViz', 1, "+/- = α ladder,  0 = re-fit the window", "+/- = step α through those values,  0 = redraw the plot to fit", '"ladder", "re-fit the window"')
add('PowerViz', 1, "Enter = menu,  Esc = exit and export", "Enter = menu,  Esc = quit; the results stay in Home (EP_PWR and the rest)", '"export"')
add('PowerViz', 1, "t(df) = t obtained if a sample had these values", "t(df) = the t that a sample with exactly these values would give", 'telegraphic')
add('PowerViz', 2, "the dashed red line = set α by hand; on lift it snaps to the ladder if within 15 %",
    "the dashed red line = set α by hand; when you lift your finger, α jumps to the nearest of those values if it is within 15 % of it", '"on lift", "snaps", "ladder"')
add('PowerViz', 2, "up or down = n (one step per 12 px)", "up or down = change n (one step for every 12 pixels)", 'telegraphic')
add('PowerViz', 2, "α, zcrit = the α ladder;", "α, zcrit = step through the α values;", '"ladder"')
add('PowerViz', 2, "pale magenta = H₁ before", "pale magenta = H₁ before your last change", 'before what')
add('PowerViz', 3, "then the z values put in (PPL): the number.", "then the program puts in the z values (PPL), giving the number.", 'telegraphic')
add('PowerViz', 3, "2-sided: it drops the far tail,", "2-sided: the formula leaves out the tail on the far side,", '"it drops"')
add('PowerViz', 3, "no CAS: the formula is shown as texts print it.", "no CAS: the formula is shown as textbooks print it.", '"texts"')
add('PowerViz', 4, "box: n, μ, σ by group", "the box shows n, μ and σ for each group", 'telegraphic')
add('PowerViz', 5, "how often would Levene's test notice at your n? (A plan.)",
    "how often would Levene's test detect the difference at your n? (For planning a study.)", '"notice", "(A plan.)"')

# ---------------------------------------------------------------- RankLab
add('RankLab', 1, "slot 4 (Exact/Normal or the page's toggle),", "the 4th key (Exact/Normal, or what that page switches),", '"slot 4", "toggle"')
add('RankLab', 2, "+ = slot 4 (Exact/Normal, ranks/values, rs/ tau-b);", "+ = the 4th soft key (Exact/Normal, ranks/values, rs/tau-b);", '"slot 4"')
add('RankLab', 2, "Slot 4 shows what is on now.", "The 4th soft key's label shows which choice is on now.", '"slot 4", "what is on"')
add('RankLab', 5, "0 = the blocks disagree, 1 = all rank alike.", "0 = the blocks disagree, 1 = every block ranks the treatments the same.", 'telegraphic')
add('RankLab', 5, "Halo: 11 criteria order 8 judges, W only (no p).", "Halo preset: the same 8 judges ranked on 11 criteria; W only, no p (the same lawyers rated every criterion).", 'cryptic')
add('RankLab', 5, "Lower = a negative association.", "Lower (one-sided) tests for a negative association.", 'telegraphic')
add('RankLab', 6, "p ≥ 0.05 is no evidence of a difference, not proof of none.",
    "p ≥ 0.05 means no evidence of a difference; it is not proof that there is none.", 'hard to parse')

# ---------------------------------------------------------------- ResampLab
add('ResampLab', 1, "Once: the pooled values are dealt again into groups of the same sizes, and their difference d drops onto the histogram.",
    "Once: the pooled values are shuffled into new groups of the same sizes, and the new difference d is added to the histogram.", '"dealt", "drops onto"')
add('ResampLab', 1, "Assumes: under H₀ the labels are exchangeable (random assignment).",
    "Assumes: under H₀ the labels could be swapped without changing anything, which is true when the groups were made by random assignment.", '"exchangeable" unexplained')
add('ResampLab', 3, "(a stack = picked more than once)", "(a stack of dots = a value picked more than once)", 'telegraphic')
add('ResampLab', 3, "Basic: those ends reflected about the estimate.", "Basic: the same two ends, mirrored around the estimate.", '"reflected about"')
add('ResampLab', 3, "Small samples give too narrow intervals: n ≥ 15 or so.", "With small samples the intervals are too narrow: use n of about 15 or more.", 'telegraphic')

# ---------------------------------------------------------------- RiskLab
add('RiskLab', 2, "Speed: each pass touches every row;", "Speed: each step of the fit goes through every row;", '"pass touches"')
add('RiskLab', 4, "Choosing a cut-off chooses which error costs more: the statistics show the trade, they do not set the price.",
    "Choosing a cut-off is choosing which error matters more: the statistics show the trade-off, but they cannot say which error is worse.", '"set the price"')
add('RiskLab', 5, "A score (COMPAS): pred = RiskLab's own fit.", "For a score such as COMPAS's, pred is the P from RiskLab's own logistic fit of Y on the score.", 'telegraphic')
add('RiskLab', 6, "Both sides' numbers can be right at once: different questions.",
    "Both sides' numbers can be right at once, because they answer different questions.", 'telegraphic')

# ---------------------------------------------------------------- SampDist
add('SampDist', 1, "σx̄ = σ / SQRT(n).", "σx̄ = σ / √n.", 'calculator syntax in prose')
add('SampDist', 1, "Three curves, shared axes: 4× n halves σx̄.", "Three curves on the same axes: four times the n gives half the standard error.", 'telegraphic')
add('SampDist', 1, "Results persist in Home as EP_SD_*", "Results are kept in Home as EP_SD_ names.", '"persist", "*"')
add('SampDist', 2, "on ONE scale: at n = 30 the population's peak is 18% of x̄'s.",
    "on ONE scale: at n = 30 the population curve's peak is only 18% as high as the x̄ curve's.", 'telegraphic')
add('SampDist', 2, "Tail  next region;", "Tail  the next kind of region (left, right, between, outside);", 'telegraphic')
add('SampDist', 2, "Critical values: a new n moves them (α kept).", "Critical values: changing n moves them; α stays the same.", 'telegraphic')

# ---------------------------------------------------------------- ScatterLab
add('ScatterLab', 2, "the squared misses of the flat line at ȳ.", "the squared distances of the points from the flat line at ȳ.", '"misses"')

# ---------------------------------------------------------------- StatDist
add('StatDist', 1, "Menus: the tail first, then the form.", "Then two menus: choose the tail first, then fill in the form.", 'telegraphic')
add('StatDist', 1, "on lift x snaps to the grid.", "when you lift your finger, x moves to the nearest grid value.", '"on lift", "snaps"')
add('StatDist', 1, "+/- = zoom, 0 = refit the window.", "+/- = zoom, 0 = redraw the plot to fit.", '"refit the window"')
add('StatDist', 2, "Zoom-, Zoom+ = about x.", "Zoom-, Zoom+ = zoom out or in around x.", 'telegraphic')
add('StatDist', 2, "More (slot 6) = the next page:", "More (the 6th soft key) = the next set of keys:", '"slot 6", "page"')
add('StatDist', 2, "Approx / N(0,1) = the overlay (else Refit),", "the 4th key = Approx (the normal approximation, for the binomial and Poisson), N(0,1) (behind t), or Refit (the others),", '"(else Refit)"')
add('StatDist', 3, "More again = page 3:", "More again = the third set of keys:", '"page 3"')

# ---------------------------------------------------------------- StudRange
add('StudRange', 1, "Tukey HSD: n = total k means", "Tukey HSD: n = k, the number of means", 'telegraphic')
add('StudRange', 1, "Newman-Keuls: n = span of pair", "Newman-Keuls: n = the means from the pair's lower to its higher, both counted", '"span of pair"')
add('StudRange', 1, "Duncan: N-K q, α* = 1-(1-α)^(n-1)", "Duncan: Newman-Keuls's q, at α* = 1-(1-α)^(n-1)", 'abbreviation')
add('StudRange', 1, "df = 0 → ν = ∞ (plain range dist)", "df = 0 means ν = ∞ (the range itself, σ known)", '"plain range dist"')
add('StudRange', 1, "After Dunlap et al. 1977, BRMI 9(4)", "After Dunlap et al. 1977, Behav Res Meth Instr 9(4)", '"BRMI"')
add('StudRange', 2, "q is the range (the largest pair), so q > q crit has chance α for the whole family.",
    "q uses the range (the largest mean minus the smallest), so q > q crit has chance α for the whole family of pairs.", '"the largest pair"')
add('StudRange', 3, "Diagnostics probes Python live.", "Diagnostics checks that Python is working.", '"probes ... live"')
add('StudRange', 3, "Python errors are silent here: test with the Terminal open (hardware).",
    "Python's errors are not shown here; to see them, run it with the Terminal open, on a calculator.", 'telegraphic')
add('StudRange', 4, "Drag in the plot: q obs (p sweeps)", "Drag in the plot: move q obs (p changes as you go)", '"p sweeps"')
add('StudRange', 4, "Drag the right edge: α (CDF height)", "Drag the right edge: set α (as a height on the CDF)", 'telegraphic')
add('StudRange', 4, "Menu modes: full precision  Plot: fast grid (curve-level)", "Menu answers: full precision.  Plot: a faster grid, close but not exact.", 'cryptic')

# ---------------------------------------------------------------- SurvLab
add('SurvLab', 2, "n.r. = open.", "n.r. (not reached) = no upper end.", '"open"')
add('StudRange', 1, "Verified vs Harter 1960 tables", "Checked against Harter's 1960 tables", '"vs"')
add('StatDist', 3, "each checked against the program;", "each checked against the program's own numbers;", '"against the program"')

# ---------------------------------------------------------------- TTestLab (and TTestLabG: the same first page)
for pg in ('TTestLab', 'TTestLabG'):
    add(pg, 1, "SOFT KEYS:  1 H, 2 df, 3 crit, 4 t, 5 end = the five steps;  Menu = the menu",
        "SOFT KEYS: the five steps, 1 H (the hypotheses), 2 df, 3 crit (t crit), 4 t (t obt), 5 end (the decision);  Menu = the menu", 'the key names are abbreviations')
    add(pg, 1, "Left / Right = a step back / on", "Left / Right = the step before / the next step", '"a step back / on"')
    add(pg, 1, "MENU: edit the numbers, tails and α, pooled or separate side by side, choose the test, examples",
        "MENU: Edit the numbers; Tails and α; Pooled or separate? (the two tests side by side); Choose the test; Examples", 'the menu items run together')
    add(pg, 1, "sample 1 (or x₁) in D1, sample 2 (or x₂) in D2",
        "sample 1 in D1 and sample 2 in D2 (for pairs, each pair's x₁ in D1 and its x₂ in D2)", '"(or x₁)" unexplained')
    add(pg, 2, "Cohen's d: pooled s (independent); sD (pairs)", "Cohen's d divides by the pooled s (two groups) or by sD (pairs)", 'telegraphic')
    add(pg, 2, "(Pooled checked = pooled)", "(tick Pooled for the pooled test)", 'telegraphic')
add('TTestLab', 2, "t crit: exact for your df, and the printed table's row (df 73 -> row 60, as the lecture)",
    "t crit: the exact value for your df, and the printed table's value (a df the table lacks uses the next smaller row: df 73 uses row 60)", '"as the lecture" means nothing to a reader of the book (TTestLab follows your lecture: keep it if you want your own students to see it)')
add('TTestLab', 2, "Step 4 keeps 4 significant digits on the way; rounding sooner can move t obt (see example 1)",
    "Step 4 keeps 4 significant digits at each step; rounding sooner can change t obt (see example 1)", '"on the way"')
add('TTestLab', 2, "Welch-Satterthwaite df, as SPSS", "Welch-Satterthwaite df, as SPSS prints them", 'telegraphic')
add('TTestLab', 2, "Group 1 minus group 2, as the lecture and SPSS", "The difference is group 1 minus group 2, as in SPSS", '"as the lecture", as in change 5')
add('TTestLabG', 2, "A printed table: a df it lacks, the next smaller row; a fractional df, rounded down first.",
    "With a printed table, a df it lacks uses the next smaller row, and a fractional df is rounded down first.", 'telegraphic')
add('TTestLabG', 2, "Step 4 keeps 4 significant digits on the way.", "Step 4 keeps 4 significant digits at each step.", '"on the way"')
add('TTestLabG', 2, "Group 1 minus group 2, as SPSS and R do", "The difference is group 1 minus group 2, as in SPSS and R", 'telegraphic')

# ---------------------------------------------------------------- TestChooser
add('TestChooser', 1, "Ordinal, or skewed, or tiny n → ranks:", "Ordinal, or skewed, or a very small n → ranks:", '"tiny n"')
add('TestChooser', 1, "Two variables linked?", "Are two variables related?", '"linked"')
add('TestChooser', 1, "The table is from Glantz's Primer of Biostatistics, with a one-sample column.",
    "The table follows Glantz's Primer of Biostatistics, with a column added for one sample.", 'whose column?')
add('TestChooser', 2, "Tap a row name or a heading to light it up (+ = row, - = column).",
    "Tap a row name or a column heading to highlight it (or + for the row, - for the column).", '"light it up"')
add('TestChooser', 2, "The corner key shows the one-sample column.",
    "The box in the top-left corner switches to the one-sample column (so does Left from the first column).", '"the corner key" is not a key')
add('TestChooser', 2, "Hatched cells: not on the Prime (R, JMP).", "Hatched cells: tests the Prime does not run (use R or JMP).", 'telegraphic')

# ---------------------------------------------------------------- TrendTest
add('TrendTest', 1, "1 df concentrates the evidence: more power than Pearson when the line really fits.",
    "With 1 df the trend test puts all its evidence into one question, so it has more power than Pearson's when the proportions really do lie near a straight line.", '"concentrates the evidence", "the line really fits"')
add('TrendTest', 1, "Pearson - trend = departure from linearity (k-2 df); large means 'not a straight line'.",
    "Pearson's χ² minus the trend χ² (k-2 df) measures how far the proportions are from a straight line; a large value means they do not follow one.", 'formula-speak')
add('TrendTest', 1, "The trend answer depends on the spacing; Pearson's does not.",
    "The trend test's answer depends on how the scores are spaced; Pearson's does not.", '"the spacing" of what?')
add('TrendTest', 1, "Press Scores: 1,2,3 / as entered / midranks.",
    "The Scores key switches among 1, 2, 3 ..., the scores as entered, and midranks.", 'telegraphic')
add('TrendTest', 2, "the weighted (WLS) line in magenta with its 95% band; overall p dotted.",
    "the weighted least-squares (WLS) line in magenta, with its 95% band; the overall proportion as a dotted line.", '"overall p dotted"')
add('TrendTest', 2, "the line tilts, the band and the tests follow.", "the line, its band, and the tests change with it.", '"follow"')
add('TrendTest', 2, "Odds ratio plot: each level against level 1, log scale: 0.5 and 2 lie equally far from 1; Woolf 95% intervals; dotted line = OR 1.",
    "Odds ratio plot: each level's odds ratio against level 1, on a log scale (so 0.5 and 2 lie equally far from 1), with Woolf 95% intervals; the dotted line is OR = 1.", 'telegraphic')
add('TrendTest', 2, "Results page 4: where the line comes from.", "Page 4 of the results shows how the line is worked out.", '"where the line comes from"')
add('TrendTest', 3, "Keys: ⇆ = level, ⇅ = cases,", "Keys: ⇆ = choose a level, ⇅ = change its cases,", 'telegraphic')
add('TrendTest', 3, "Results: 4 pages, ⇆ or tap.", "The results run to 4 pages; turn them with ⇆ or a tap.", 'telegraphic')
add('TrendTest', 3, "The proportions plot animates the fit as it opens (any key or tap skips).",
    "The proportions plot draws the fit step by step as it opens (any key or tap skips to the end).", '"animates the fit"')
add('TrendTest', 3, "as this page does;", "as TrendTest does;", '"this page"')

# ---------------------------------------------------------------- TDist3D
add('TDist3D', 1, "This surface stacks the curves:", "This surface puts the curves one behind another:", '"stacks"')
add('TDist3D', 1, "Every row has area 1.  The front rows are low in the middle and lifted in the tails; the back rows rise toward N(0,1), the gray dots past the back edge: ν = ∞ is the normal curve itself.",
    "Every curve has area 1.  The front curves (small ν) are low in the middle and high in the tails; the back curves come close to N(0,1), the normal curve, drawn as gray dots beyond the back edge (ν = ∞).", '"row" of what? (Roger, 17q: "any row of WHAT")')
add('TDist3D', 2, "By ν = 30, the price of estimating σ is small.", "By ν = 30, using s in place of σ makes little difference.", '"the price of estimating σ"')
add('TDist3D', 3, "Slice marks one row, ν = ν₀, in red, and the corner gives its numbers:",
    "Slice draws one curve, ν = ν₀, in red, and the corner gives that curve's numbers:", '"row"')
add('TDist3D', 3, "The red posts stand at ±t crit when they fall inside t = ±6; at ν = 1 they do not (12.7).",
    "The red posts mark ±t crit when it lies inside t = ±6; at ν = 1 it does not (12.7).", 'small')
add('TDist3D', 3, "ν− and ν+ climb a ladder:", "ν− and ν+ step ν through", '"climb a ladder"')
add('TDist3D', 3, "Menu > Set ν exactly takes values in between.", "For a value in between, use Menu > Set ν exactly.", 'order')
add('TDist3D', 4, "Drag: sideways turns, downward raises the eye.", "Drag sideways to turn the surface; drag down to look at it from higher up.", '"raises the eye"')
add('TDist3D', 4, "Arrows: Left, Right turn; Up, Down raise and lower the eye; 10° a step.",
    "Arrows: Left and Right turn it; Up and Down look from higher or lower; 10° a press.", '"raise the eye"')
add('TDist3D', 4, "Curves: the family seen end on; 3-D goes back.", "Curves: all the curves seen flat, from the front; 3-D goes back to the surface.", '"seen end on"')
add('TDist3D', 4, "and a tap on a curve picks it.", "and tapping a curve makes it the slice.", '"picks it"')
add('TDist3D', 4, "Home after a run: TD_NU holds ν.", "After a run, TD_NU in Home holds the last ν.", 'telegraphic')
add('EpiStats', 5, "coverage than Wald, esp. for small n).", "coverage than Wald, especially for small n).", 'abbreviation')
add('EpiStats', 5, "OR/RR: log method - compute CI on ln(OR), then exponentiate.", "OR/RR: the log method: find the CI for ln(OR), then take e to the power of each end.", '"exponentiate"')
add('NormExplorer', 2, "PAGE 2: WHAT ← → MOVE", "SECOND SET OF KEYS: WHAT ← AND → MOVE", '"PAGE 2" is the second set of soft keys, not help page 2')
add('NormExplorer', 2, "the lower bound (or x₀), the upper", "A = the lower bound (or x₀), B = the upper", 'which is which')
add('NormExplorer', 2, "μ; or σ, ← narrower → wider", "μ = the mean; σ = ← narrower, → wider", 'telegraphic')

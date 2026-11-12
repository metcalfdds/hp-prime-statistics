# FDAES Student Guide

Oct 19, 2026 · @Roger Dale Metcalf Sr

FDAES (Forensic Dental Age Estimation Suite) runs seven published dental age methods on the HP Prime and pools their answers; this guide shows how to use it and, method by method, what each number assumes. It describes FDAES v3.9c (v3.9b with symbols on screen, such as ≥ for ">="; v3.9b reworded one page of v3.9a: see "Where these errors came from").

*Roger D. Metcalf, DDS, JD, DFSc, 2026. Written with AI assistance: the program's concept, direction and decisions, and all testing on the calculator, are the author's; the code, the drafting of this guide and the checking of its sources were done with Claude Opus 5.5 and Claude Fable 5.1 (Anthropic) in October 2026.*

## What FDAES is, and what it is not

> **Disclaimer.** FDAES, like every program in this collection, is a teaching and demonstration aid. It is not validated forensic or casework software, and its results must not be relied on for legal purposes. A qualified examiner checks every number against the original papers.

FDAES answers a teaching question: what do the published dental methods say about this person's age, and how sure can they be that the person is 18 or older?

- **It is** a way to watch each method's arithmetic on real inputs, to compare methods side by side, and to see what each method cannot tell you (ceilings, floors, large errors in the young and the old).
- **It is not** an expert opinion, a substitute for the radiographs, measurements and published tables, or a tool validated on any casework sample.

In court it is the method, its reference sample and the examiner's judgment that are tested. A calculator's printout adds nothing to them, and every assumption in this guide is a question a cross-examiner can ask.

## Getting started

A case in FDAES runs Setup first, then the methods that fit the person, then the pool. Every result page offers to add its estimate to the pool once.

&#91;embedded content: a case in FDAES · Setup, three groups of methods, the pool\]

M3 stands apart: it gives a probability for one stage, not an age, so it never enters the pool.

**Loading it.** FDAES comes as a text file. In HP's Connectivity Kit, create a new program named FDAES, paste the whole file, and save. On the calculator open the Program Catalog (Shift, then Program), select FDAES and press Check: a clean compile shows no message. Run it from the Catalog, or type FDAES in Home. On the Virtual Calculator, type the name without empty parentheses.

**A case, step by step:**

1. **Read the opening notice.** FDAES is a teaching and demonstration aid, not casework software.
2. **Setup.** Sex (Unknown, Male, Female) picks the boys' or girls' tables for Willems, Liversidge and M3, and the Prince & Ubelaker equation. Ancestry (Unknown, White, Black, Other) matters only for Prince & Ubelaker, whose sample had white and black people only.
3. **Run the methods that fit the person.** A child or teenager: stage the seven teeth on the odontogram (Willems and Liversidge). A third molar: M3, which gives a probability, not an age. An adult: Lamendin / Prince-Ubelaker, Johanson, Bang & Ramm.
4. **Add each result to the pool once.** One result per tooth: never both Lamendin and Prince & Ubelaker for one tooth, and never both Willems and Liversidge for one set of staged teeth.
5. **More options → Bayesian Combination.** The pooled estimate, its SD, P(age ≥ 18) and the band; a forest plot of the methods; a plot of the pooled curve where you can type any threshold age; and a report template.
6. **More options → Clear / New Case** before the next person.

**The two menu screens.**

| Screen 1 | Screen 2 (More options) |
| --- | --- |
| Setup: sex & ancestry | Johanson 1971 histology |
| Willems 2001 subadult (the odontogram; also gives Liversidge) | Bang & Ramm 1970 |
| M3 Threshold P(age ≥ 18) | Bayesian Combination |
| Lamendin / Prince-Ubelaker | Threshold Table |
| How to use / assumptions (ten help topics) | Clear / New Case |
| More options... | Verify Calculations |
| Exit | About & Methods |

The help topics on the calculator follow this guide's sections in short form: Using FDAES, one topic per method, Assumptions, and What FDAES is not.

## Children and teenagers: Willems 2001 and Liversidge 2006

Both methods read the same seven teeth, the left mandibular teeth 31 to 37, each staged A to H on a panoramic radiograph. Willems adds the seven teeth's scores into one age; Liversidge averages each tooth's typical age at its stage. Neither can say how old a person is once all seven teeth are mature.

**Staging the teeth (Demirjian, Goldstein & Tanner 1973).** In FDAES you tap each tooth on the odontogram and choose its stage from the pictures. The rules that matter most:

- Each stage has one to three criteria; the previous stage's criteria must also be met (p 221).
- "In borderline cases the earlier stage is always assigned" (p 221).
- No measuring: crown and root lengths are compared by eye or with dividers (p 221).

| Stage | What you see (uniradicular teeth; Demirjian pp 221–226) |
| --- | --- |
| A | Calcified cusp tips, not yet joined |
| B | Cusps fused into a regular occlusal outline |
| C | Enamel complete at the occlusal surface; dentine beginning |
| D | Crown complete to the cemento-enamel junction; root just starting |
| E | Root shorter than the crown |
| F | Root as long as the crown or longer; apex funnel-shaped |
| G | Root canal walls parallel; apex still partly open |
| H | Apex completely closed; periodontal space even around the root |

**Willems et al. (2001).** Belgian children's radiographs from the University Hospitals of Leuven: 2,523 films (1,265 boys aged 1.8–18.0, 1,258 girls aged 2.1–18.0), of which 2,116 could be scored, plus a second sample of 355 films for testing (p 893).

- Each tooth's stage has a score in years (Table 1 boys, Table 2 girls); **the sum of the seven scores is the dental age** (p 894).
- FDAES's spread is the paper's own test: dental minus real age had SD 0.9 yr for boys and 1.3 yr for girls, with mean errors 0.0 and +0.2 (p 894). With the sex unknown, FDAES uses a 50:50 mix of the boys' and girls' answers.
- **The ceiling.** The boys' table tops out at 16.03 yr, all seven at H. The girls' table tops out at 15.93 yr, not at all-H (15.79), because its G scores for the two incisors are higher than its H scores. The sample stopped at 18.0, so a mouth at or near the top says only "at least about 16". When teeth 33 to 37 are all at H, FDAES v3.9 shows the ceiling, draws no verdict band and offers nothing to the pool.
- The authors' caution: the scores "may not be valid in other populations" (p 894).

**Liversidge et al. (2006).** A meta-analysis of 9,002 children aged 2–16.99 from eight groups (Australia, Belgium, Quebec, London, Finland, southern France, South Korea, Sweden), 4,480 girls and 4,522 boys (pp 455, 465).

- Table X gives, for each tooth and stage, the **mean age of children in that stage** and the SD of their ages (p 467). FDAES averages the seven teeth's means.
- It shows two SEs for that average: one if the teeth vary independently, a larger one if they move together, and passes on the larger.
- **The floor.** Table X has no stage H ("this would represent the age distribution", p 457). A tooth at H gives only a floor from Table IX: the mean age at which children reach H. If a floor sits above the estimate, FDAES draws no verdict band.
- The authors' caution: "Considerable heterogeneity was noted between groups" (p 455).

## The third molar: Mincer 1993

Mincer, Harris and Berryman give no age at all: they give the chance that a person whose third molar is at a given stage is 18 or older. FDAES shows that chance and does not pool it with the age estimates.

**The sample (pp 379–380).** 823 cases sent in by 24 ABFO diplomates from the United States and parts of Canada, aged 14.1 to 24.9, 54 % female, 80 % white and 19 % black; 74 % of the films were panoramic. Table 4 is for white subjects only. Stages A, B and C were too rare in this age range to use.

**Table 4 as corrected by the 1993 erratum: P(age ≥ 18), %, white subjects (p 384; erratum p 1524).**

| Jaw and sex | D | E | F | G | H |
| --- | --- | --- | --- | --- | --- |
| Maxilla, males | 15.9 | 27.8 | 44.0 | 46.8 | 85.3 |
| Maxilla, females | 9.7 | 28.4 | 50.4 | 63.3 | 89.6 |
| Mandible, males | 6.1 | 29.4 | 40.5 | 56.0 | 90.1 |
| Mandible, females | 11.3 | 27.4 | 43.2 | 69.8 | 92.2 |

The original printing gave 69.4 for mandible, males, E; the erratum corrects it to 29.4. The 2010 textbook chapter by Harris, Mincer, Anderson and Senn still prints 69.4 (Forensic Dentistry, 2nd ed., Table 13.12, p 289), so check which version a source uses.

**How FDAES reads the stage.** It colours the result by the authors' own words, not by a cut-point of its own: stage D "unlikely to be 18"; E, F and G "essentially a coin toss (50:50)" (p 387); H "reasonably confident", with a caveat.

**The stage-H caveat.** "Grade H (apex closed) occurs in all mature third molars regardless of age" (p 387). Table 4's H figures assume the person is under 25. A closed apex says nothing about whether someone is 19 or 59, so the H figure holds only if other evidence already rules out an older adult.

**The authors' own limits.** The third molar "is far from an ideal developmental marker" (p 386); Too few blacks were available "to yield reliable estimates" (p 381); 24 examiners scored the films, which "introduced greater variability" (p 380).

## Adults, single-rooted teeth: Lamendin 1992 and Prince & Ubelaker 2002

Both methods use three measurements on the labial surface of a whole single-rooted tooth, with no sectioning. FDAES always gives Lamendin's estimate, and adds Prince & Ubelaker's when Setup gives a sex and white or black ancestry; only one of the two goes to the pool.

**What you measure, in mm (Lamendin pp 1374–1375):**

1. **Root height (RH):** from the apex to the cemento-enamel junction.
2. **Periodontosis height:** the greatest distance from the cemento-enamel junction to the line of soft-tissue attachment.
3. **Translucency height:** from the apex, the greatest height of the translucent zone, seen against a light box.

FDAES turns these into Lamendin's two percentages: **P = periodontosis × 100 / RH** and **T = translucency × 100 / RH**. Lamendin measured with a calliper and ruler, "precision of the measure is ± 1 mm" (p 1375).

**Lamendin et al. (1992): A = 0.18 P + 0.42 T + 25.53** (p 1375).

- Sample: 306 single-rooted teeth, free of restorations, from 208 people (135 men, 73 women; 198 white, 10 black), aged 22 to 90 (p 1374). The country is not stated; the authors worked in France.
- Errors reported: a mean error of 10 yr on that sample (Table 1), 8.4 yr on 45 forensic teeth (Table 2), and 8.9 yr against Gustafson's 14.2 yr on 39 other people (p 1377). The 14.2 is Gustafson's error, not Lamendin's.
- **FDAES's spread is 12.5 yr.** Lamendin calls his figure the average difference between actual and estimated age and does not say whether signs were ignored; FDAES reads it, like Prince & Ubelaker's, as the average size of a miss, which is not an SD. For normally distributed errors the SD is the mean error × √(π/2) = 1.25 × 10 = 12.5. Prince & Ubelaker's own four groups show the same ratio, 1.28 to 1.32 (next paragraph). It is also the more conservative choice.
- The authors' limits: "reasonably accurate except for cases of individuals under age 40" (p 1373); the constant "makes the latter useless for individuals under 25" (p 1376).

**Prince & Ubelaker (2002).** They tested Lamendin's method on the Terry Collection at the Smithsonian (skeletons collected 1900–1965): 400 teeth from 359 people aged 25 to 99 (pp 107–108). Ancestry alone made no significant difference; sex did. They then fitted one equation per group, adding root height in mm. FDAES uses the equations as printed in their text:

| Group | Equation (A in years) | SEE, yr | Source |
| --- | --- | --- | --- |
| Black males | 1.04 RH + 0.31 P + 0.47 T + 1.70 | 8.12 | Table 3, p 112 |
| White females | 1.10 RH + 0.31 P + 0.39 T + 11.82 | 10.41 | Table 4, p 113 |
| Black females | 1.63 RH + 0.48 P + 0.48 T − 8.41 | 11.90 | Table 5, p 114 |
| White males | 0.15 RH + 0.29 P + 0.39 T + 23.17 | 9.58 | Table 6, p 115 |

- **SEE** is each regression's root mean square error: the SD of its misses. Their "mean difference" figures (6.24, 8.11, 9.19, 7.25 yr, Table 7) are mean absolute misses, about 1.3 times smaller.
- The printed coefficients round the tables' estimates, and two of them not to the nearest figure: black males' RH is 1.0488 in Table 3, printed 1.04; white males' is 0.1587, printed 0.15. At typical measurements this moves the age by under 0.2 yr.
- Each group had 100 teeth in its regression (99 for white males); the Terry sample has no other ancestry groups, so FDAES uses no P-U equation for "Unknown" or "Other". Outside the Terry sample's ages (25 to 99), FDAES shows P-U's estimate as an extrapolation, with no band and no pool entry.
- The authors' limits: "the younger individuals were overestimated in age while the older individuals were underestimated" (p 109); "significant error may be possible with individual cases" (p 116); "we recommend that this technique be utilized in conjunction with others" (p 116).

## Adults, histology: Johanson 1971

Johanson scores six changes on a thin ground section of the tooth and weights them by how well each predicts age. Root transparency carries the most weight.

**What you score.** Each tooth is ground to 0.25 mm through the pulp, and each change is scored 0 to 3 in half steps: **A** attrition, **S** secondary dentine, **P** periodontal recession, **C** cementum apposition, **R** root resorption, **T** root transparency. Attrition and the periodontal state are recorded before extraction, and transparency before the section is mounted.

**The equation (Table 5, line VI):**

```latex
\text{Age} = 11.02 + 8.98\,T + 5.14\,A + 4.14\,P + 5.57\,R + 3.71\,C + 2.30\,S
```

The sample: 162 teeth from 46 people (31 men, 15 women) aged 23 to 79. 98 % were incisors, canines and one-rooted premolars. The country and years of collection are not stated in the pages consulted.

**A misprint to know about.** Johanson's running text prints **9.98T**; his Table 5 and his worked example print **8.98T**. The worked example (A 2, S 1, P 1, C 1, R 0, T 1.5) gives 44.92 yr only with 8.98. FDAES uses 8.98. At T = 2.5 the two differ by 2.5 years.

**What the spread is.**

- **5.16 yr** is the SD of the misses of the six-variable fit (r = 0.92), but over 46 *people* rather than single teeth: 42 of them gave 2 to 11 teeth and 4 gave one, and "the 'mouth' (2 teeth or more) has been the entity". FDAES uses it for two or more teeth. It does not make it smaller for more teeth: in an independent test, a shrinking error proved too small, with only 53 % of estimates inside it (Lucy, Pollard & Roberts 1995).
- **Table 8** gives an error by the number of teeth averaged: 6.0 yr for one tooth, 5.2 for two, 4.9 for three, falling to 4.4 for ten. The table does not say what kind of error it is. Its 5.2 for two teeth sits beside the fit's SD of 5.16, though, and Johanson calls his error figures standard deviations.
- **6.0 yr** has been FDAES's spread for a single tooth since v3.9a (Roger's decision). It is Johanson's own Table 8 figure. An independent test on 35 roots from 17 new people found an average miss of 4.5 yr, an SD of about 5.6 for normal errors, with about 68 % of estimates within ±5.16 (Lucy, Pollard & Roberts 1995). That was a small test, so new cases may miss by more. FDAES v3.9 and earlier used 8.00, a number of its own with no source.

**Limits.** The equation was tested only on the 46 people it was fitted to: no independent validation sample appears in the paper. Johanson's own advice: "age determination in the hand of the unexperienced is not advisable", and an examiner "should make his own regression line". A dead pulp gives "only ... the lowest age for that individual".

*The copy of Johanson used for this guide is a partial scan with few printed page numbers, so page citations for this monograph are left out here.*

**Why FDAES leaves out Gustafson (1950).** Gustafson scored six changes 0 to 3 and simply added them (pp 47–49). He built his line from 41 teeth and claimed an error of ±3.63 yr (p 51). Maples and Rice (1979) found three problems with this:

- The same teeth were used to build the line and to test it.
- The published line cannot be reproduced from the real ages; Maples and Rice concluded it was fitted to Gustafson's own estimated ages.
- The 3.63 is not the spread of a single estimate. Maples and Rice took it for a mean deviation; Aykroyd (1995) showed it is the error of a predicted average, worked out with the wrong SD. Refitted on the real ages, one estimate's standard error is ±7.03 yr (pp 168–170), the same figure Johanson had found in 1971.

Tested on 39 other people, Gustafson's method missed by 14.2 yr on average, and Lamendin's by 8.9 (Lamendin 1992, p 1377). Lucy and colleagues add that summed 0–3 scores are ordinal data, which regression handles poorly (1996, p 189).

The lesson runs through this whole guide: measure a method's error on people it was not built from. Johanson's equation was tested that way only later, on 17 people (Lucy, Pollard & Roberts 1995). For single roots its quoted error held up. When several roots were combined, the error it predicted was too small.

## Adults, root transparency: Bang & Ramm 1970

Bang and Ramm measure one thing, the length of transparent dentine from the root apex in millimetres, and give a separate equation for every tooth and side. FDAES v3.9 uses their own four tables (pp 21–24).

**What you measure.** X is TM: the mean of the shortest and the longest extent of transparent dentine from the apex (p 4), on the intact root (IT) or on a 0.4 mm longitudinal section (SS). Molars are pooled: Bang and Ramm grouped the corresponding roots of all six molars in each jaw (p 19), so you choose upper or lower molar and then the root (mesial, distal and, for upper molars, palatal).

**In FDAES.** Choose intact root or section, then the tooth, then the side (or, for a molar, the root), then type X in mm:

- **X ≤ 9.0 mm:** A = B0 + B1·X + B2·X², from Table VIII (intact) or IX (section).
- **X > 9.0 mm:** A = B0 + B1·X, from Table X (intact) or XI (section).
- The spread is that row's **SA**, the SD of the misses in that row's fit.

**Worked example.** Lower left lateral incisor, intact root, X = 6.0 mm. Table VIII's row gives B0 = 18.58, B1 = 10.25, B2 = −0.538, SA = 10.08, so A = 18.58 + 10.25×6 − 0.538×36 = **60.7 yr**, SD 10.1 yr.

**The switch at 9.0 mm.** The two tables were fitted separately, so they do not meet exactly. For the same tooth, X = 9.0 gives 67.3 yr (Table VIII) and X = 9.01 gives 65.5 yr (Table X): a jump of 1.8 years for a hundredth of a millimetre. FDAES warns when X is near 9.0.

**Several roots from one person (p 21).** Age each root separately, then:

```latex
A = \frac{1}{n}\sum_{i=1}^{n} a_i \qquad S_A = \frac{1}{n}\sqrt{\sum_{i=1}^{n} S_{a_i}^2 + 85\,n(n-1)}
```

The 85·n(n−1) term allows for teeth from one mouth being alike (they correlated 0.80 to 0.90, p 11). When several teeth are available, Bang and Ramm advise leaving out upper first premolars and all molars (p 19). Without it, two roots with SA 10 each would give 7.1 yr; with it they give 9.6 yr, barely better than one root. FDAES offers "Another root, same person?" and pools only the combined value. It refuses the same root entered twice (an intact reading and a section of one root count as the same root).

**Table XII (p 24).** Bang and Ramm give their own coverage: A ± 0.45·SA "ca. 35 %", A ± SA "ca. 65 %", A ± 2·SA "ca. 95 %". (For normal errors ± 1 SD covers 68 %.)

**The sample (pp 4–6).** 926 teeth (978 roots): 450 extracted from 201 patients in a mental institution (112 men, 89 women) and 476 from 64 autopsies (46 men, 18 women), aged from their teens to over 80. The country is not stated; the authors worked in Bergen.

**Their own test, and its limit.** On 168 teeth from 24 new people aged 26 to 85, 19 of the 24 fell within ± SA (p 22). But "in older people, however, there seemed to be a tendency for underestimation of age" (p 22): the four oldest, aged 75.8 to 85.9, came out 17.5 to 20.4 years too young (Table XIII, p 25). FDAES refuses an estimate above 110 yr and warns when X passes 14 mm, the end of their figures.

## Pooling the methods

FDAES combines the estimates you add to its pool by weighting each one by its precision, then widens the result twice on purpose, because the methods are not truly independent. The page is headed "Bayesian Combination"; strictly it is a weighted average with two safety margins.

**The arithmetic.** Each estimate mᵢ with spread SDᵢ gets the weight wᵢ = 1 / SDᵢ²:

```latex
\bar{m} = \frac{\sum w_i\,m_i}{\sum w_i} \qquad \text{SD}_{\text{pool}} = \max\!\left(1.25\,\sqrt{\frac{1}{\sum w_i}},\ \text{smallest single SD}\right)
```

- **Why × 1.25.** The formula assumes the methods' errors are independent. They are not: Lamendin, Prince & Ubelaker, Johanson and Bang & Ramm all read root transparency, often on the same teeth, by the same examiner. The 1.25 is FDAES's own allowance for that; no paper gives it.
- **Why the floor.** Without it, pooling can claim more precision than any method has. The pooled SD is never allowed below the best single method's SD. This is also FDAES's own rule.
- **One result per tooth.** Lamendin and Prince & Ubelaker on the same tooth are the same evidence, so FDAES lets you pool only one of them; likewise Willems or Liversidge for one set of staged teeth, and only the combined value for several Bang & Ramm roots.

**Worked example (from FDAES's own self-check).** A white man; one tooth measured for Prince & Ubelaker, two or more teeth scored for Johanson, and two roots for Bang & Ramm:

| Method | Estimate, yr | SD, yr | Weight |
| --- | --- | --- | --- |
| Prince & Ubelaker, white males | 46.82 | 9.58 | 18.1 % |
| Johanson, 2+ teeth | 45.99 | 5.16 | 62.4 % |
| Bang & Ramm, two roots combined | 63.11 | 9.23 | 19.5 % |

The weighted mean is 49.47 yr. The unwidened SD is 4.08 yr; × 1.25 gives 5.09 yr; the floor then raises it to 5.16 yr, Johanson's own SD. The pooled answer is 49.5 ± 5.2 yr, no more precise than the best single method.

## The verdict band and P(age ≥ 18)

Under a result, FDAES draws a coloured band that sorts P(age ≥ 18) into three zones at stated cut-points of 5 % and 95 %. The cut-points are printed in the band so no one has to guess where they came from.

| P(age ≥ 18), as printed | Band | Words |
| --- | --- | --- |
| 95 % or more | green | probably ≥ 18 |
| more than 5 %, less than 95 % | orange | uncertain |
| 5 % or less | red | probably < 18 |

**Where the probability comes from.** FDAES treats the estimate m and its spread SD as a normal curve and takes the area at 18 and above: P = Φ((m − 18) / SD). On the calculator it is computed as the mirror-image lower tail, NORMALD\_CDF(m, SD, 2m − 18), because 1 − CDF loses every digit once the tail is smaller than about 5 × 10⁻¹³.

**What a wide spread does.** Lamendin's SD is 12.5 yr, so an adult method needs a large estimate before the band turns green:

- Lamendin estimate 25 yr: P = 71 %, **uncertain**.
- Lamendin estimate 30 yr: P = 83 %, **uncertain**.
- Lamendin estimate 40 yr: P = 96 %, **probably ≥ 18**. Green needs m ≥ 18 + 1.645 × 12.5 ≈ 38.6 yr.
- Lamendin's formula never gives less than 25.5 yr (P = T = 0), so its P(age ≥ 18) never falls below 72.7 %: it can never say "probably < 18". Lamendin himself called it "useless for individuals under 25" (p 1376).

**When FDAES draws no band:**

- Willems at the tables' ceiling: teeth 33 to 37 all at H.
- Liversidge when a tooth at H sets a floor above the estimate.
- Prince & Ubelaker outside its sample's ages (25 to 99), where its estimate is an extrapolation.
- M3 (Mincer), which uses the authors' own words for each stage instead.

**What the probability is not.** It is a normal-curve figure under that method's reference sample, not a measured frequency and not the chance that this person is an adult "in fact". The next section explains why it depends on who was in the reference sample.

## The assumptions behind every number

Every number FDAES prints rests on the assumptions below. When one fails, the number is wrong in a direction you can predict, and each is a fair question in cross-examination.

| Assumption | Where it enters | When it fails |
| --- | --- | --- |
| Each method's misses are normal, with the stated SD | every ± line, the 68 % and 95 % lines, P(age ≥ 18), the band | Probabilities near 0 % or 100 % are overconfident if real misses have heavier tails |
| The person resembles the reference sample: population, era, health, age range | every estimate | A systematic bias of unknown size; Willems warns his scores "may not be valid in other populations" (p 894) |
| Estimates lean toward the reference sample's ages (age mimicry) | Lamendin, Prince & Ubelaker, Johanson, Bang & Ramm, Liversidge's in-stage means | The young come out older and the old younger; P(age ≥ 18) shifts with the sample's age mix |
| The pooled methods are independent | the pool | The pooled SD is too small; hence FDAES's own × 1.25 and floor |
| The measurements and stages are read as the authors read them | every method | Lamendin's precision is ± 1 mm (p 1375); Mincer's films were scored by 24 examiners (p 380); one stage off moves Willems's sum |

**Normal misses.** Several papers report a mean error, not an SD. For normal misses the SD is 1.25 times the mean error, which is how Lamendin's 10 yr becomes FDAES's 12.5 yr. Prince & Ubelaker's own groups give ratios of 1.28 to 1.32, a little above 1.25, which hints that real misses have slightly heavier tails than the normal curve.

**Age mimicry.** A regression of age on a dental feature is fitted to one sample, and its estimates lean toward that sample's ages. As one textbook puts it, "age estimates tend to mimic the structure of the known-age reference sample" (İşcan & Steyn 2013, p 88). The signature is a U-shaped error: large misses at both ends of the age range, small ones in the middle, where most of the reference sample sits.

&#91;embedded content: Lamendin et al. 1992, Table 1 (306 teeth) · Prince & Ubelaker 2002, Table 2 (400 teeth) · Lamendin's formula on both\]

A single "mean error of 10 years" hides this shape: in middle age the formula is good to about 6 years, at either end it is off by 13 to 33. The end bands are small (5 to 19 teeth each), but both samples show the same U.

The same pattern shows in Bang & Ramm's test, where the four oldest people came out 17.5 to 20.4 years too young (p 25). Applied to new groups, the Bang & Ramm equations over-aged the young and under-aged the old (Tang, Le Cabec & Antoine 2016, p 211). Liversidge's in-stage means carry the same effect, because the mean age of the children in a stage depends on which children were sampled (Liversidge 2015).

**Why it matters for the 18 question.** P(age ≥ 18) is computed as if the estimate were unbiased. For a young person it usually is not: the methods built on adults tend to make the young look older. So a "probably ≥ 18" from an adult method, for someone who might be a minor, deserves particular caution.

## Worked case and practice questions

**The case.** A young man with no documents says he is 17. On his panoramic radiograph all seven left mandibular teeth are at stage H, and the lower right third molar is at stage G. Setup: Male.

1. **Willems:** all seven at H is the ceiling, 16.03 yr for boys. FDAES says "at least about 16", draws no band and pools nothing.
2. **Liversidge:** every tooth at H gives only floors; the largest is the second molar's, the mean age at which boys reach H, 15.25 yr. FDAES says "at least 15.25" and gives no estimate.
3. **M3 (Mincer):** mandible, male, stage G: P(age ≥ 18) = 56.0 % (Table 4 as corrected). The authors call stages E to G "essentially a coin toss".

**Conclusion.** His teeth say he is at least about 16. They are equally consistent with 17 and with 25. The pool is empty, and the honest answer is that the teeth cannot settle the question. That is FDAES working as intended: a method that cannot see past its ceiling says so.

**Practice questions** (answers below).

1. A girl's seven teeth are all at H. What does Willems tell you, and why does FDAES offer nothing to the pool?
2. Lamendin gives 30 yr. What is P(age ≥ 18), and which band does FDAES draw?
3. Why does FDAES use 12.5 yr, not 10 yr, as Lamendin's spread?
4. A white woman's tooth: root height 14 mm, periodontosis 4 mm, translucency 7 mm. Work out P, T, Lamendin's age and Prince & Ubelaker's age.
5. Bang & Ramm, lower left lateral incisor, intact root: why do X = 9.0 mm and X = 9.01 mm give ages 1.8 years apart?
6. Two roots from one person each have SA = 10 yr. What is the combined S\_A, and why is it not 7.1 yr?
7. Johanson's text and his Table 5 disagree on the coefficient of T. Which does FDAES use, and what evidence decides it?
8. Why should a "probably ≥ 18" from an adult method be treated with extra caution for someone who may be a minor?
9. Johanson's equation has an SD of 5.16. Why does FDAES use 6.0 for a single tooth?

**Answers.**

1. Only that she is at least about 16. Her all-H sum, 15.79, sits at the top of the girls' table (whose maximum, 15.93, needs the two incisors at G). A sum at the ceiling is a floor, not an age, so there is nothing honest to average.
2. P = Φ((30 − 18) / 12.5) = Φ(0.96) = 83 %: orange, "uncertain". Green would need 95 %.
3. Lamendin reports a mean error. For normal misses SD = mean error × √(π/2) = 1.25 × 10 = 12.5; Prince & Ubelaker's own ratios (1.28–1.32) support it.
4. P = 4 × 100 / 14 = 28.6; T = 7 × 100 / 14 = 50. Lamendin: 0.18 × 28.6 + 0.42 × 50 + 25.53 = 51.7 yr (SD 12.5). Prince & Ubelaker, white females: 1.10 × 14 + 0.31 × 28.6 + 0.39 × 50 + 11.82 = 55.6 yr (SEE 10.41).
5. Up to 9.0 mm the quadratic Table VIII applies, above it the straight-line Table X. The two were fitted separately and do not meet.
6. S\_A = ½ √(100 + 100 + 85 × 2 × 1) = 9.6 yr. Roots from one mouth are alike; treating them as independent (½ √200 = 7.1) would overstate the precision.
7. 8.98, from Table 5. His own worked example gives 44.92 yr only with 8.98.
8. Adult methods were fitted to adults and lean toward adult ages (age mimicry), so a young person's estimate is pushed up. The probability assumes no such bias.
9. 5.16 is the fit's SD over 46 people, most of whom gave two or more teeth, and one tooth carries less information. Johanson's own Table 8 gives 6.0 for one tooth. An independent test on 17 new people found single-root misses averaging 4.5 yr, an SD of about 5.6 (Lucy, Pollard & Roberts 1995). So 6.0 is sourced and a little on the safe side.

## What changed in v3.9 and v3.9a, and why

On 19 October 2026 FDAES v3.8a was checked line by line against the papers it uses, and the fixes went into v3.9 and v3.9a. One rule applied throughout: **every number must come from a paper, with its page, or be labelled as FDAES's own choice.** Where the papers left room for a choice, Roger Metcalf made it, and he took the more conservative option.

| What | Before | Now (v3.9a) | Why, and the source |
| --- | --- | --- | --- |
| Lamendin's spread | SD 10.0 for European ancestry, 10.5 to 12.5 for the others | SD 12.5 for everyone | Lamendin reports a mean error of 10 yr (Table 1). A mean error is not an SD: for normal errors SD = 10 × √(π/2) = 12.5. Prince & Ubelaker's groups show the same ratio (1.28–1.32). It is also the more conservative value (Roger). |
| Lamendin's constant | 27.00 Unknown, 25.53 European, 29.69 African American, 27.21 Asian, 26.50 Hispanic | 25.53 for everyone | Lamendin prints only 25.53 (p 1375). The other four appear in neither Lamendin nor Prince & Ubelaker, whose sample had no Asian or Hispanic people. |
| Prince & Ubelaker | The ancestry constants above | Their four equations (sex × white or black), with root height in mm. SD = each equation's RMSE: 8.12, 10.41, 11.90 or 9.58 yr | Tables 3–6, pp 112–115, transcribed twice and checked (Roger). |
| P-U outside its sample | Used like any estimate | Below 25 or above 99 yr: shown as an extrapolation, with no band and no pool entry | Their sample was aged 25 to 99 (p 108). |
| Bang & Ramm | One line per tooth on transparency as a percentage (tooth 13: 13.9 + 1.43 × T %), with spreads not in the paper | Their own tables: TM in mm, a curve up to 9.0 mm and a straight line above, each row with its own SA | Tables VIII–XI, pp 21–24, transcribed twice (Roger). |
| Bang & Ramm, several roots | Not offered | A = the mean of the roots; S\_A = (1/n)√(ΣSa² + 85·n(n−1)) | Their own rule (p 21). The 85·n(n−1) term allows for roots from one mouth being alike. |
| Johanson, one tooth | SD 8.00, FDAES's own number with no source | SD 6.0 | Johanson's Table 8 gives 6.0 for one tooth, and its value for two teeth (5.2) matches the fit's SD of 5.16. An independent test on 17 new people found an average miss of 4.5 yr, which is an SD of about 5.6 (Lucy, Pollard & Roberts 1995). Roger chose 6.0. |
| Johanson, two or more teeth | SD 5.16 | SD 5.16, unchanged and now labelled | The fit's SD over 46 people (Table 5). FDAES does not shrink it for more teeth, because the same test found a shrinking error too small. |
| Willems, all seven teeth at H | A dental age with a band ("P(age ≥ 18) = 1.4 %") and an offer to pool | "At least about 15.8–16 yr", with no band and no pool entry. The same applies when teeth 33 to 37 are all at H | A sum at the top of the tables is a floor, not an age. The sample stopped at 18.0 (p 893). The girls' largest sum is 15.93, not the all-H 15.79 (Table 2). Roger confirmed the 33–37 rule. |
| Liversidge, a tooth at H above the estimate | Band drawn | No band | A tooth at H means the person is probably past the average age at which children reach H (Table IX). An estimate below that average contradicts it. |
| Verdict band | "Likely ≥ 18" from 83 %, "likely < 18" below 58 %, with no source | "Probably ≥ 18" from 95 %, "probably < 18" at 5 % or less, with the cut-points printed in the band | The old cut-points came from a ladder that no paper gives. Under them, 83 % (a one-in-six chance of a child) read "likely ≥ 18", and 57 % (more likely an adult than not) read "likely < 18" (Roger). |
| P(age ≥ 18) near 0 or 100 % | v3.8 computed 1 − CDF and printed "0.0 %" under "< 0.1 %" | The mirror-image lower tail (since v3.8a) | The Prime keeps 12 digits, so 1 − CDF becomes exactly 0 once the tail is below about 5 × 10⁻¹³. |
| Interval ends above 110 yr | Cut off at "110.0" | Printed as "> 110" | A cut-off end looks like a measurement, and no method was built on people that old. |
| Gustafson's error | "SE 14.2 (39-tooth test)", credited to Lamendin | Gustafson's mean error 14.2 yr on 39 people; Lamendin's own, 8.9 yr | Lamendin 1992, p 1377. Gustafson's own ±3.63 is not the error of one estimate (Aykroyd 1995); refitted, one estimate's SE is ±7.03 (Johanson 1971; Maples & Rice 1979, p 170). |
| Prince & Ubelaker citation | J Forensic Sci 47(3):519–523 | 47(1):107–116 | The paper's own first page. |
| The history pages | Saunders (1837) "warned against teeth" and "Parliament ignored him"; unsourced Gustafson and ABFO lines | Rewritten from the papers (v3.9a) | Saunders argued *for* teeth (pp 45, 49). The other sources are Cattell 1928 (pp 67, 71), Saunders et al. 1993 (p 173), Harris et al. 2010 (p 289), the ABFO 2011 workshop and the 2017 ABFO manual. |

**Numbers that stay as they were, and why:**

- **Johanson's 8.98 T.** His running text prints 9.98, but his Table 5 prints 8.98, and only 8.98 reproduces his own worked example (44.92 yr).
- **Mincer's Table 4, mandible, males, stage E: 29.4 %.** The 1993 erratum corrects the original 69.4. The 2010 textbook chapter by Harris and colleagues still prints 69.4 (Table 13.12, p 289), so check which version a source uses.
- **The pool's × 1.25 and its floor.** Both are FDAES's own safety margins, and are labelled so. No paper gives them.

## Where these errors came from

Several of the numbers corrected above were not FDAES's own inventions. They had travelled through the published literature for decades: Gustafson's ±3.63 read as the error of one estimate, Lamendin's mean error read as an SD, Mincer's misprinted 69.4 and a second wrong value, 19.0, in later textbooks. The companion document **[How the Errors Propagated](https://claude.ai/artifact/VmyFzz7NqScU8UQhypmagy)** traces each of these errors from where it started, to who corrected it, to where it was still being printed afterwards, with the page for every step. It also traces FDAES's own errors back to the day the program was first written.

**What v3.9b changed (19 October 2026, night).** One page: "Why Gustafson 1950 is excluded". v3.9a said Gustafson's ±3.63 "is a mean deviation" and that his line was "fitted to estimated, not real, ages". Both were Maples & Rice's 1979 readings. The page now says: refitted on real ages the SE is ±7.03 (Maples & Rice, p 170), and "Aykroyd (1995, p 925): 3.63 is the error of a predicted mean, using the wrong SD; not one estimate's". No number, table or equation changed.

**What v3.9c changed (20 October 2026).** Only the text on screen: symbols instead of spelled-out names, as in this guide. FDAES now shows P(age ≥ 18), ±, ≤, √(π/2), μ and σ where it showed "P(age >= 18)", "+/-", "<=", "sqrt(pi/2)", "mu" and "sigma". No number, table, equation or band changed.

Two papers matter most for this guide:

- **Aykroyd (1995)** showed what Gustafson's ±3.63 really is: the error of a predicted *average* age, computed with the sample SD of the ages, not the error of one person's estimate (p 925).
- **Lucy & Pollard (1995)** showed that Gustafson's line could not be recalculated and that age had been regressed on the scores "the wrong way round" (pp 223–224).

## Sources

Every figure in this guide, and every number and historical statement in FDAES v3.9a, was checked against these papers, as printed. The tables FDAES uses for Prince & Ubelaker and Bang & Ramm were transcribed twice, independently, from page images and compared cell by cell.

- American Board of Forensic Odontology. *Diplomates Reference Manual*, Section IV, Standards & Guidelines, March 2017 edition: Standards and Guidelines for Dental Age Assessment.
- Aykroyd RG. Calculation of Gustafson's "error of estimation" (letter). *Journal of Forensic Sciences* 1995;40(6):925.
- American Board of Forensic Odontology. *Dental Age Estimation: Children*, workshop, Chicago, 19–20 February 2011 (J. M. Lewis's slides).
- Bang G, Ramm E. Determination of age in humans from root dentin transparency. *Acta Odontologica Scandinavica* 1970;28:3–35. Tables VIII–XIII, pp 21–25; procedure pp 20–21.
- Cattell P. *Dentition as a Measure of Maturity*. Harvard Monographs in Education no. 9. Cambridge, MA: Harvard University Press; 1928. pp 67, 71.
- Demirjian A, Goldstein H, Tanner JM. A new system of dental age assessment. *Human Biology* 1973;45(2):211–227. Stages A–H, pp 221–226.
- Gustafson G. Age determinations on teeth. *Journal of the American Dental Association* 1950;41:45–54. pp 47–52.
- Harris EF, Mincer HH, Anderson KM, Senn DR. Age estimation from oral and dental structures. In: Senn DR, Stimson PG, eds. *Forensic Dentistry*, 2nd ed. Boca Raton: CRC Press; 2010. Table 13.12, p 289.
- İşcan MY, Steyn M. *The Human Skeleton in Forensic Medicine*, 3rd ed. Springfield IL: Charles C Thomas; 2013. Age mimicry, p 88.
- Johanson G. Age determinations from human teeth. *Odontologisk Revy* 1971;22(Suppl 21). Table 5, line VI; Table 8.
- Lamendin H, Baccino E, Humbert JF, Tavernier JC, Nossintchouk RM, Zerilli A. A simple technique for age estimation in adult corpses: the two criteria dental method. *Journal of Forensic Sciences* 1992;37(5):1373–1379.
- Liversidge HM, Chaillet N, Mörnstad H, Nyström M, Rowlings K, Taylor J, Willems G. Timing of Demirjian's tooth formation stages. *Annals of Human Biology* 2006;33(4):454–470. Tables IX and X, pp 465–467.
- Liversidge HM. Controversies in age estimation from developing teeth. *Annals of Human Biology* 2015 (early online).
- Lucy D, Aykroyd RG, Pollard AM, Solheim T. A Bayesian approach to adult human age estimation from dental observations by Johanson's age changes. *Journal of Forensic Sciences* 1996;41(2):189–194.
- Lucy D, Pollard AM. Further comments on the estimation of error associated with the Gustafson dental age estimation method. *Journal of Forensic Sciences* 1995;40(2):222–227. pp 222–224.
- Lucy D, Pollard AM, Roberts CA. A comparison of three dental techniques for estimating age at death in humans. *Journal of Archaeological Science* 1995;22:417–428.
- Maples WR, Rice PM. Some difficulties in the Gustafson dental age estimations. *Journal of Forensic Sciences* 1979;24(1):168–172.
- Mincer HH, Harris EF, Berryman HE. The A.B.F.O. study of third molar development and its use as an estimator of chronological age. *Journal of Forensic Sciences* 1993;38(2):379–390; erratum, *Journal of Forensic Sciences* 1993, p 1524 (Table 4, mandible, males, grade E: 29.4, not 69.4).
- Prince DA, Ubelaker DH. Application of Lamendin's adult dental aging technique to a diverse skeletal sample. *Journal of Forensic Sciences* 2002;47(1):107–116. Tables 2–7, pp 109–115.
- Saunders E. *The Teeth a Test of Age, Considered with Reference to the Factory Children*. Addressed to the members of both Houses of Parliament. London: Renshaw; 1837. pp 45–49.
- Saunders S, DeVito C, Herring A, Southern R, Hoppa R. Accuracy tests of tooth formation age estimations for human skeletal remains. *American Journal of Physical Anthropology* 1993;92:173–188.
- Tang N, Le Cabec A, Antoine D. Dentine and cementum structure and properties. In: Irish JD, Scott GR, eds. *A Companion to Dental Anthropology*. Wiley Blackwell; 2016. p 211.
- Willems G, Van Olmen A, Spiessens B, Carels C. Dental age estimation in Belgian children: Demirjian's technique revisited. *Journal of Forensic Sciences* 2001;46(4):893–895.

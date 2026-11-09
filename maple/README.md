# The Maple t surface

Student's t density as one surface over *t* and the degrees of freedom ν, drawn in Maple by Roger D. Metcalf. It is Figure 9.3 of *Statisticles*, and TDist3D (`programs/TDist3D_beta1.txt`) is the calculator's version of it: the same surface, turned with a finger, with the critical value of any row read off a red slice.

## What is here

| File | What it is |
|---|---|
| `MapleTdistribution.mw` | The Maple worksheet (Maple 2020.2, saved 17 May 2024). Open it in Maple; it is not a text file. |
| `t_surface_1d.mpl` | The same work as plain Maple input (1-D), for reading on GitHub or pasting into a Maple session. Written from the worksheet; see the note below. |
| `MapleTDistribution1.png` … `4a.png` | Views of the surface exported from the worksheet in 2024. `4a` has the two arrows that Figure 9.3 uses. |
| `tPlot1.JPG` … `tPlot4.JPG` | Four earlier views, watermarked "© Roger Metcalf 2022": the conventional view, "rotated a bit," "looking from side," and "looking from back left." |

## What the worksheet does

The worksheet is in Maple's document mode, with the density typed in as 2-D math and the rest done from the Context Panel, whose actions appear as the section titles. In order:

1. **The density.** `f(t) = Γ((ν+1)/2) / (√(νπ) Γ(ν/2)) · (1 + t²/ν)^(−(ν+1)/2)`, assigned to `Ex`.
2. **Solve for t** (the Context Panel's solve, with `explicit` and `dropmultiplicity`).
3. **3D Plot.** The surface itself: `plot3d` of the right-hand side over *t* and ν. The plots show *t* from −10 to 10 and ν from 0 to 10.
4. **Simplify.**
5. **Differentiate With Respect to nu.** ∂f/∂ν; Maple's answer brings in the digamma function Ψ.
6. **Differentiate Both Sides With Respect to nu.**
7. **Differentiate With Respect to t.** ∂f/∂t.
8. **Integrate With Respect to t.** ∫ f dt, which Maple gives as a hypergeometric function.
9. **Expand** and **Normalize** the right-hand side.

## A note on the 1-D file

Maple stores 2-D input as typeset math, not as text, so `t_surface_1d.mpl` is a transcription, not an export: the density and the operations are the worksheet's, read from its typeset input, and the plot ranges are read from the axes of the plots it produced (the worksheet does not store the Context Panel's ranges as text). To get Maple's own text of the worksheet, open `MapleTdistribution.mw` in Maple and use File → Export As → Maple Input (`.mpl`).

## Credit

The surface, the worksheet, and the plots: Roger D. Metcalf, 2022–2024, first drawn while hunting for a distribution to model the long right tail of the data for his doctoral capstone (the hunt ended at the Burr XII; see `docs/burrlab-guide.md`). The 1-D transcription and this note: Claude (Anthropic), 8 November 2026.

*Free for educational and personal use. © 2026 Roger D. Metcalf.*

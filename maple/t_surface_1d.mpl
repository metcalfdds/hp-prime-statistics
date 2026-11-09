# t_surface_1d.mpl -- Student's t density as a surface over t and nu, in plain Maple input.
# A 1-D transcription of MapleTdistribution.mw (Roger D. Metcalf, Maple 2020.2, 17 May 2024), whose input is typeset
# 2-D math built with the Context Panel.  The density and the operations are the worksheet's; the plot ranges are read
# from the axes of the plots it produced (t from -10 to 10, nu from 0 to 10).  Transcribed by Claude, 8 November 2026.
# Paste into a Maple session, or read it as it is.  TDist3D does the same surface on the HP Prime.

restart;

# 1. The density, assigned to Ex (the worksheet's name for it)
Ex := f(t) = GAMMA((nu + 1)/2) / (sqrt(nu*Pi) * GAMMA(nu/2)) * (1 + t^2/nu)^(-(nu + 1)/2);

# 2. Solve for t (the Context Panel's "Solve for t", explicit, one root each)
solve({Ex}, t, explicit, dropmultiplicity);

# 3. The surface: f over t and nu (the Context Panel's "3D Plot"; the ranges are those of the saved plots)
plot3d(rhs(Ex), t = -10 .. 10, nu = 0 .. 10, axes = boxed, labels = ["t", "nu", "pdf"]);

# 4. Simplify
simplify(Ex);

# 5. Differentiate with respect to nu (Maple's answer uses the digamma function, Psi)
diff(rhs(Ex), nu);

# 6. Differentiate both sides with respect to nu
diff(Ex, nu);

# 7. Differentiate with respect to t
diff(rhs(Ex), t);

# 8. Integrate with respect to t (Maple answers with a hypergeometric function)
int(rhs(Ex), t);

# 9. Expand the right-hand side, and normalize the equation
expand(rhs(Ex));
normal(Ex);

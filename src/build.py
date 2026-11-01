#!/usr/bin/env python3
"""Build the booklets:  python3 src/build.py [basic|extension]

For each booklet (both, unless one is named):
1. Checks every practice answer in its content file: expressions must equal
   their question (tested at many random values) and be simplified / fully
   factorised; equations, inequalities, tables and story rules are checked
   by substituting values. Any problem stops the build.
2. Writes booklet/<name>.tex from the content file.
3. Runs pdflatex (twice) to make the PDF in the repository root.
"""
import math
import os
import random
import re
import shutil
import subprocess
import sys

import importlib

sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX_DIR = os.path.join(ROOT, "booklet")

BOOKLETS = {
    "basic": {"module": "content", "tex": "algebra-basic-skills",
              "pdf": "Algebra-Basic-Skills-Booklet.pdf"},
    "extension": {"module": "content_extension", "tex": "algebra-extension",
                  "pdf": "Algebra-Extension-Workbook.pdf"},
}
C = None  # the content module of the booklet being built

# ---------------------------------------------------------------------------
# Answer checking
# ---------------------------------------------------------------------------

def to_python(expr):
    """'3x^2 + 2(x - 1)' -> '3*x**2+2*(x-1)'. Variables are single letters."""
    s = expr.replace(" ", "").replace("×", "*")
    if "÷" in s:
        num, den = s.split("÷")
        s = f"({num})/({den})"
    s = s.replace("^", "**")
    out = []
    for ch in s:
        if out:
            prev = out[-1]
            if (prev.isdigit() or prev.isalpha() or prev == ")") and (ch.isalpha() or ch == "("):
                out.append("*")
        out.append(ch)
    return "".join(out)


def same(q, a, trials=40):
    q_py, a_py = to_python(q), to_python(a)
    letters = sorted(set(re.findall(r"[a-z]", q + a)))
    rng = random.Random(1)
    for _ in range(trials):
        env = {v: rng.uniform(0.5, 5) * rng.choice([1, -1]) for v in letters}
        if not math.isclose(eval(q_py, {}, env), eval(a_py, {}, env), rel_tol=1e-9, abs_tol=1e-9):
            return False
    return True


def terms(expr):
    """'3x^2 - 2x + 5' -> ['3x^2', '-2x', '+5'] (no brackets expected)."""
    return re.findall(r"[+-]?[^+-]+", expr.replace(" ", ""))


def letter_part(term):
    t = re.sub(r"^[+-]?\d*", "", term)
    powers = {}
    for v, p in re.findall(r"([a-z])(?:\^(\d+))?", t):
        powers[v] = powers.get(v, 0) + int(p or 1)
    return tuple(sorted(powers.items()))


def check_simplified(a):
    problems = []
    if any(c in a for c in "×÷()"):
        problems.append("answer still has ×, ÷ or brackets")
    parts = [letter_part(t) for t in terms(a)]
    if len(parts) != len(set(parts)):
        problems.append("answer has like terms that weren't collected")
    if any(re.match(r"^[+-]?1[a-z]", t) for t in terms(a)):
        problems.append("answer writes a coefficient of 1")
    return problems


def check_factorised(a):
    problems = []
    mo = re.fullmatch(r"(-?\d*[a-z]*)\((.*)\)", a.replace(" ", ""))
    if not mo:
        return ["answer is not in the form  factor(bracket)"]
    inside = terms(mo.group(2))
    coeffs = [int(re.match(r"[+-]?(\d*)", t).group(1) or 1) for t in inside]
    if math.gcd(*coeffs) != 1:
        problems.append("a number factor is left inside the bracket")
    if set.intersection(*[set(re.findall(r"[a-z]", t)) for t in inside]):
        problems.append("a letter factor is left inside the bracket")
    return problems


def split_sub(q):
    """'3a + 2b | a = 2, b = 3' -> ('3a + 2b', {'a': 2, 'b': 3})"""
    expr, vals = q.split("|")
    env = {k.strip(): int(v) for k, v in (pair.split("=") for pair in vals.split(","))}
    return expr.strip(), env


REL = r"\s*(<=|>=|<|>|=)\s*"


def split_rel(q):
    """'2x - 5 < 7' -> ('2x - 5', '<', '7')"""
    lhs, op, rhs = re.split(REL, q.strip())
    return lhs, op, rhs


def value(expr, env):
    return eval(to_python(expr), {}, env)


def holds(lhs, op, rhs, env):
    l, r = value(lhs, env), value(rhs, env)
    return {"<": l < r - 1e-9, ">": l > r + 1e-9, "<=": l <= r + 1e-9,
            ">=": l >= r - 1e-9, "=": abs(l - r) < 1e-9}[op]


def check_solve(eq, sol):
    """The solution makes the equation true, and nothing else nearby does."""
    lhs, op, rhs = split_rel(eq)
    var, _, val = split_rel(sol)
    v = float(eval(to_python(val)))
    if op != "=" or not holds(lhs, "=", rhs, {var: v}):
        return [f"'{sol}' does not solve '{eq}'"]
    if holds(lhs, "=", rhs, {var: v + 1}):
        return [f"'{eq}' is true for other values too"]
    return []


def check_ineq(q, a):
    """Same truth value as the question either side of, and at, the boundary."""
    lhs, op, rhs = split_rel(q)
    var, aop, val = split_rel(a)
    v = float(val)
    for t in (v - 0.5, v, v + 0.5):
        if holds(lhs, op, rhs, {var: t}) != holds(var, aop, val, {var: t}):
            return [f"'{a}' does not match '{q}' at {var} = {t}"]
    return []


def check_rule(a, pts):
    var_out, _, rhs = split_rel(a)
    var_in = (set(re.findall(r"[a-z]", rhs.lower())) or {"x"}).pop()
    bad = [(i, o) for i, o in pts if not math.isclose(value(rhs, {var_in: i}), o)]
    return [f"'{a}' gives the wrong output for input {i} (expected {o})" for i, o in bad]


def norm(s, item):
    """Every question becomes a dict with a 'type'. Plain strings/tuples use the section's kind."""
    if isinstance(item, str):
        return {"type": "expr", "kind": s["kind"], "q": item}
    if isinstance(item, tuple):
        return {"type": "expr", "kind": s["kind"], "q": item[0], "a": item[1]}
    return dict(item)


def check_item(it):
    t = it["type"]
    if t == "expr":
        q, a = it["q"], it["a"]
        if it["kind"] == "substitute":
            expr, env = split_sub(q)
            return [] if math.isclose(value(expr, env), float(a)) else [f"'{q}' does NOT equal {a}"]
        errs = [] if same(q, a) else [f"'{q}' is NOT equal to '{a}'"]
        probs = check_factorised(a) if it["kind"] == "factorise" else check_simplified(a)
        return errs + [f"'{q}' -> '{a}': {p}" for p in probs]
    if t == "solve":
        return check_solve(it["q"], it["a"])
    if t == "word":
        return check_solve(it["eq"], it["sol"])
    if t == "ineq":
        return check_ineq(it["q"], it["a"])
    if t == "table":
        return check_rule(it["a"], list(zip(it["x"], it["y"])))
    if t == "rule":
        return check_rule(it["a"], it["pts"])
    if t == "written":
        return [] if it.get("a", "").strip() else ["written question has no model answer"]
    return [f"unknown question type '{t}'"]


def check_question_only(it):
    """Skill Check questions: must make sense, and must NOT carry an answer."""
    if any(k in it for k in ("a", "eq", "sol", "pts")):
        return ["Skill Check questions must not include an answer"]
    t = it["type"]
    if t == "expr":
        if it["kind"] == "substitute":
            expr, env = split_sub(it["q"])
            value(expr, env)
        else:
            to_python(it["q"])
    elif t in ("solve", "ineq"):
        lhs, _op, rhs = split_rel(it["q"])
        var = re.findall(r"[a-z]", lhs + rhs)[0]
        value(lhs, {var: 1}), value(rhs, {var: 1})
    elif t == "table" and len(it["x"]) != len(it["y"]):
        return ["table rows are different lengths"]
    return []


def check_all():
    errors, count = [], 0
    for s in C.SECTIONS:
        for i, item in enumerate(s["practice"], 1):
            count += 1
            errors += [f"Section {s['num']} practice Q{i}: {e}" for e in check_item(norm(s, item))]
        for i, item in enumerate(s["check"], 1):
            errors += [f"Section {s['num']} skill check Q{i}: {e}" for e in check_question_only(norm(s, item))]
    return count, errors


# ---------------------------------------------------------------------------
# LaTeX rendering
# ---------------------------------------------------------------------------

def mbody(expr):
    s = expr.replace("×", r"\times ").replace("÷", r"\div ")
    s = s.replace("<=", r"\le ").replace(">=", r"\ge ")
    s = re.sub(r"(\w+)/(\w+)", r"\\frac{\1}{\2}", s)
    return re.sub(r"\^(\d+)", r"^{\1}", s)


def m(expr):
    return f"${mbody(expr)}$"


def qtex(q, compact=False):
    """A question for a box. Substitution questions also show their values."""
    if "|" not in q:
        return m(q)
    expr, vals = (x.strip() for x in q.split("|"))
    vals = ", ".join(m(v.strip()) for v in vals.split(","))
    if compact:
        return m(expr) + r"\\[1pt]{\normalsize when " + vals + "}"
    return m(expr) + r"\enspace{\large when " + vals + "}"


def brace_args(text, pos, n):
    """Read n balanced {...} groups starting at text[pos]. Returns (args, end)."""
    args = []
    for _ in range(n):
        assert text[pos] == "{", text[pos:pos + 40]
        depth, start = 0, pos
        while True:
            depth += {"{": 1, "}": -1}.get(text[pos], 0)
            pos += 1
            if depth == 0:
                break
        args.append(text[start + 1:pos - 1])
    return args, pos


def numline(lo, hi, width, bound=None, op=None, step=1, font=r"\scriptsize"):
    """A number line from lo to hi, width cm wide; optionally with a solution drawn on it."""
    unit = width / (hi - lo + 1.2)
    labels = f"{lo},{lo + step},...,{hi}" if step != 1 else f"{lo},...,{hi}"
    out = [r"\begin{tikzpicture}[x=%.3fcm, baseline=-1mm]" % unit,
           r"\draw[thick,<->,>=stealth] (%g,0) -- (%g,0);" % (lo - 0.6, hi + 0.6),
           r"\foreach \k in {%d,...,%d} \draw (\k,0.09) -- (\k,-0.09);" % (lo, hi),
           r"\foreach \k in {%s} \node[below=-1pt, font=%s] at (\k,-0.09) {$\k$};" % (labels, font)]
    if bound is not None:
        end = hi + 0.55 if op in (">", ">=") else lo - 0.55
        fill = "accent" if op in ("<=", ">=") else "white"
        out.append(r"\draw[accent, line width=2pt, ->, >=stealth] (%g,0) -- (%g,0);" % (bound, end))
        out.append(r"\draw[accent, thick, fill=%s] (%g,0) circle (2.4pt);" % (fill, bound))
    out.append(r"\end{tikzpicture}")
    return "".join(out)


def rich(text):
    """Convert \\example{q}{steps}{ans}, @@numline lo hi bound op width@@ and `maths` in LaTeX notes."""
    out, pos = [], 0
    for mo in re.finditer(r"(?m)^\\example(?=\{)", text):
        if mo.start() < pos:
            continue
        (q, steps, ans), end = brace_args(text, mo.end(), 3)
        q = q if "\\" in q else qtex(q, compact=True)
        ans = ans if "\\" in ans else m("= " + ans)
        out += [text[pos:mo.start()], r"\example{%s}{%s}{%s}" % (q, steps, ans)]
        pos = end
    text = "".join(out) + text[pos:]

    def nl(mo):
        lo, hi, b, op, w = mo.group(1).split()
        return numline(int(lo), int(hi), float(w), int(b), op)
    text = re.sub(r"@@numline ([^@]+)@@", nl, text)
    return re.sub(r"`([^`]+)`", lambda mo: m(mo.group(1)), text)


PREAMBLE = r"""% ------------------------------------------------------------------
% @@TITLE@@ booklet.
% GENERATED by src/build.py from src/@@MODULE@@.py -- edit @@MODULE@@.py and
% re-run the build, so every practice answer gets re-checked.
% ------------------------------------------------------------------
\documentclass[12pt,a4paper]{article}
\usepackage[a4paper,top=1.4cm,bottom=1.8cm,left=1.5cm,right=1.5cm,footskip=0.8cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[scaled=0.95]{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{amsmath,amssymb}
\usepackage[table]{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{enumitem,multicol,array,tabularx,pifont,fancyhdr,titlesec}

\definecolor{accent}{HTML}{1D6B8C}
\definecolor{accentlight}{HTML}{E3F0F6}
\definecolor{checkcol}{HTML}{8A3B12}
\definecolor{checklight}{HTML}{F6E7DE}
\definecolor{muted}{HTML}{56616B}
\definecolor{good}{HTML}{2E7D32}
\definecolor{warm}{HTML}{FFF6DD}
\definecolor{warmedge}{HTML}{E3B341}

\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\newcommand{\cmark}{\textcolor{good}{\ding{51}}}
\newcommand{\xmark}{\textcolor{red!70!black}{\ding{55}}}
\newcommand{\tickbox}{{\Large$\square$}}
\titleformat*{\subsection}{\large\bfseries\color{accent}}
\titlespacing*{\subsection}{0pt}{8pt}{4pt}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\footnotesize\color{muted}@@TITLE@@}
\fancyfoot[R]{\footnotesize\color{muted}Page \thepage}

% --- boxes -----------------------------------------------------------------
\tcbset{base/.style={enhanced, arc=2mm, boxrule=0.8pt, left=3mm, right=3mm, top=1.5mm, bottom=1.5mm}}
\newtcolorbox{tipbox}[1]{base, fontupper=\large, colframe=accent, colback=white, before upper={\textbf{#1.}\ }}
\newtcolorbox{stepsbox}[1]{base, fontupper=\large, colframe=accent, colback=white, before upper={\textbf{#1}\par}}
\newtcolorbox{rememberbox}{base, fontupper=\large, colframe=warmedge, colback=warm, before upper={\textbf{Remember:}\ }}
\newenvironment{examples}{\begin{tcbraster}[raster columns=3, raster equal height=rows,
  raster column skip=2.5mm, raster row skip=2.5mm, raster before skip=2mm, raster after skip=3mm]}{\end{tcbraster}}
\newcommand{\example}[3]{\begin{tcolorbox}[base, colframe=black!25, colback=white, boxrule=0.5pt, arc=1.5mm]
  {\Large #1}\par\vspace{-2pt}{\color{black!25}\rule{\linewidth}{0.4pt}}\par
  {\normalsize\color{black!75}#2}\par\vspace{2pt}
  {\Large\color{good}\boldmath #3}\end{tcolorbox}}

\newcommand{\stepnum}[2]{\tikz[baseline=(n.base)]\node[circle,fill=#2,text=white,inner sep=0pt,
  minimum size=8mm,font=\large\bfseries](n){#1};}
\newcommand{\qnum}[1]{\tikz[baseline=(n.base)]\node[circle,fill=accentlight,text=accent,inner sep=0pt,
  minimum size=6mm,font=\small\bfseries](n){#1};}
\newcommand{\cnum}[1]{\tikz[baseline=(n.base)]\node[circle,fill=checklight,text=checkcol,inner sep=0pt,
  minimum size=6.5mm,font=\small\bfseries](n){#1};}

% \banner{number}{title}{label}{colour}
\newcommand{\banner}[4]{\begin{tcolorbox}[enhanced, colback=#4, colframe=#4, arc=2mm,
  left=3mm, right=3mm, top=2mm, bottom=2mm, after skip=3mm]
  \color{white}\tikz[baseline=(n.base)]\node[circle,fill=white,text=#4,inner sep=0pt,
  minimum size=8.5mm,font=\Large\bfseries](n){#1};\hspace{3mm}{\LARGE\bfseries #2}\hfill
  \colorbox{white!20!#4}{\bfseries\MakeUppercase{#3}}\end{tcolorbox}}

% \qbox{n}{question}{height}
\newcommand{\qbox}[3]{\begin{tcolorbox}[base, height=#3, text fill, colframe=black!30, colback=white, boxrule=0.5pt,
  arc=1.5mm, top=1.5mm, bottom=2mm]\qnum{#1}\hspace{2.5mm}{\Large #2}\par\vfill
  {\Large$=$}\hspace{2mm}\textcolor{black!45}{\rule{0.8\linewidth}{0.6pt}}\end{tcolorbox}}

% \cbox{n}{question}{height}  -- skill check question, with a mark box
\newcommand{\cbox}[3]{\begin{tcolorbox}[base, height=#3, text fill, colframe=checkcol!70, colback=white, boxrule=0.8pt,
  arc=1.5mm, left=2mm, right=2mm, top=1.5mm, bottom=2mm]\cnum{#1}\hfill
  \fcolorbox{checkcol}{white}{\rule{0pt}{4.5mm}\hspace{4.5mm}}\par\vspace{1mm}
  {\large #2}\par\vfill
  {\large$=$}\hspace{1mm}\textcolor{black!45}{\rule{0.8\linewidth}{0.6pt}}\end{tcolorbox}}

% \checkhead{n}{title}{instruction}{marks}
\newcommand{\checkhead}[4]{\begin{tcolorbox}[enhanced, colback=checklight, colframe=checklight, arc=1.5mm,
  left=2mm, right=2mm, top=0.8mm, bottom=0.8mm, before skip=4mm, after skip=2mm]
  \cnum{#1}\hspace{2mm}\textbf{\color{checkcol}#2}\quad #3\hfill
  \textbf{\color{checkcol}Mark: \underline{\hspace{8mm}} / #4}\end{tcolorbox}}

\newcommand{\fillline}[1]{\textcolor{black}{\rule{#1}{0.6pt}}}
\newcommand{\ansline}[1]{\textcolor{black!45}{\rule{#1\linewidth}{0.6pt}}}

% \pbox[options]{n}{height}{body} -- a practice question of any type
\newcommand{\pbox}[4][]{\begin{tcolorbox}[base, height=#3, text fill, colframe=black!30, colback=white, boxrule=0.5pt,
  arc=1.5mm, top=1.5mm, bottom=2mm, #1]\qnum{#2}\hspace{2.5mm}#4\end{tcolorbox}}
% \kbox[options]{n}{height}{body} -- a skill check question of any type, with a mark box
\newcommand{\kbox}[4][]{\begin{tcolorbox}[base, height=#3, text fill, colframe=checkcol!70, colback=white, boxrule=0.8pt,
  arc=1.5mm, left=2mm, right=2mm, top=1.5mm, bottom=2mm, #1]\cnum{#2}\hfill
  \fcolorbox{checkcol}{white}{\rule{0pt}{4.5mm}\hspace{4.5mm}}\par\vspace{1mm}#4\end{tcolorbox}}

\begin{document}
"""


def cover():
    rows = "\n".join(
        rf"\textbf{{\color{{accent}}\large {s['num']}}} & \textbf{{{s['title']}}}\newline "
        rf"{{\small\color{{muted}}{rich(s['can'])}}} & \tickbox & \hfill/\,{len(s['check'])} \\ \hline"
        for s in C.SECTIONS)
    total = sum(len(s["check"]) for s in C.SECTIONS)
    kicker = "\\quad ".join("\\,".join(word) for word in getattr(C, "KICKER", "BASIC SKILLS BOOKLET").split())
    return rf"""
\thispagestyle{{empty}}
\begin{{tcolorbox}}[enhanced, colback=accent, colframe=accent, arc=3mm, halign=center, top=12mm, bottom=11mm]
\color{{white}}{{\small\bfseries {kicker}}}\par\vspace{{3mm}}
{{\fontsize{{34}}{{40}}\selectfont\bfseries {C.TITLE}}}\par\vspace{{3mm}}
{{\Large {C.SUBTITLE}}}
\end{{tcolorbox}}
\vspace{{10mm}}
{{\large Name: \fillline{{9.5cm}} \hfill Class: \fillline{{3.5cm}}}}

\vspace{{12mm}}
{{\Large\bfseries\color{{accent}} My progress}}\par\vspace{{2mm}}
\renewcommand{{\arraystretch}}{{2.1}}
\begin{{tabularx}}{{\linewidth}}{{|c|X|c|p{{2.4cm}}|}}
\hline
\rowcolor{{accentlight}} & \textbf{{Skill}} & \small\textbf{{Practice done}} & \small\textbf{{Skill Check}} \\ \hline
{rows}
\multicolumn{{3}}{{r|}}{{\textbf{{Skill Check total}}}} & \hfill/\,{total} \\ \cline{{4-4}}
\end{{tabularx}}
\newpage
"""


def learn_page(s):
    return (rf"\banner{{{s['num']}}}{{{s['title']}}}{{Learn}}{{accent}}" "\n"
            rf"\begin{{tcolorbox}}[enhanced, colback=accentlight, colframe=accent, boxrule=0pt, leftrule=1.5mm, arc=0mm, top=1.5mm, bottom=1.5mm]"
            rf"\textbf{{Goal:}} {rich(s['can'])}\end{{tcolorbox}}" "\n"
            + "\\large\n" + rich(s["learn"]) + "\n\\newpage\\normalsize\n")


PRACTICE_H = {"expr": "3.45cm", "solve": "3.3cm", "word": "3.5cm", "written": "7.4cm",
              "ineq": "5.0cm", "table": "3.6cm", "rule": "3.0cm"}
PRACTICE_SPAN = {"word": 2, "rule": 2}       # out of 2 columns
CHECK_SPAN = {"expr": 1, "solve": 1}         # out of 4 columns; everything else spans 2


def solve_var(q):
    return re.findall(r"[a-z]", q)[0]


def body(it, compact):
    """The inside of a question box (after the question number)."""
    t = it["type"]
    big = r"\large" if compact else r"\Large"
    txt = r"\normalsize" if compact else r"\large"
    if t == "solve":
        return (rf"{{{big} {m(it['q'])}}}\par\vfill"
                rf"{{{big} {m(solve_var(it['q']) + ' =')}}}\hspace{{2mm}}\ansline{{0.7}}")
    if t == "word":
        lines = (r" Equation:\ \ansline{0.7}\par\vspace{4mm}Answer:\ \ansline{0.4}" if compact
                 else r" Equation:\ \ansline{0.42}\hfill Answer:\ \ansline{0.3}")
        return rf"{{{txt} {rich(it['q'])}}}\par\vfill" + lines
    if t == "written":
        lines = "".join(r"\par\vspace{%s}\ansline{1}" % ("5mm" if compact else "6mm") for _ in range(3 if compact else 4))
        return rf"{{{txt} {rich(it['q'])}}}\par\vfill" + lines
    if t == "ineq":
        return (rf"{{{big} {m(it['q'])}}}\par\vfill"
                r" Answer:\ \ansline{0.4}\par\vspace{4mm}\centering " + numline(-10, 10, 7.4, step=2))
    if t == "table":
        head = " & ".join(str(v) for v in it["x"])
        row = " & ".join(str(v) for v in it["y"])
        n = len(it["x"])
        tab = (r"{\large\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|" + "c|" * n + r"}\hline"
               rf"$x$ & {head} \\ \hline $y$ & {row} \\ \hline\end{{tabular}}}}")
        return (rf"\hspace{{2mm}}{tab}\par\vfill"
                rf"{{{big} $y =$}}\hspace{{2mm}}\ansline{{0.75}}")
    if t == "rule":
        return rf"{{{txt} {rich(it['q'])}}}\par\vfill\ansline{{0.95}}"
    raise ValueError(t)


def qgrid(items, cols, height):
    boxes = "\n".join(rf"\qbox{{{i}}}{{{qtex(q)}}}{{{height}}}" for i, (q, _a) in enumerate(items, 1))
    return (rf"\begin{{tcbraster}}[raster columns={cols}, raster column skip=4mm, raster row skip=3mm]"
            f"\n{boxes}\n\\end{{tcbraster}}\n")


def practice_grid(s):
    items = [norm(s, it) for it in s["practice"]]
    if all(it["type"] == "expr" for it in items):
        return qgrid([(it["q"], it["a"]) for it in items], 2, "3.45cm")
    heights = {**PRACTICE_H, **s.get("practice_h", {})}
    boxes = []
    for i, it in enumerate(items, 1):
        t, h = it["type"], heights[it["type"]]
        if t == "expr":
            boxes.append(rf"\qbox{{{i}}}{{{qtex(it['q'])}}}{{{h}}}")
        else:
            span = PRACTICE_SPAN.get(t, 1)
            opt = f"[raster multicolumn={span}]" if span > 1 else ""
            boxes.append(rf"\pbox{opt}{{{i}}}{{{h}}}{{{body(it, compact=False)}}}")
    return (r"\begin{tcbraster}[raster columns=2, raster column skip=4mm, raster row skip=3mm]"
            "\n" + "\n".join(boxes) + "\n\\end{tcbraster}\n")


def practice_page(s):
    return (rf"\banner{{{s['num']}}}{{{s['title']}}}{{Practice}}{{accent}}" "\n"
            rf"{{\large\textbf{{{s['instr']}}}}} {{\color{{muted}}Show your working in each box.}}\par\vspace{{1mm}}" "\n"
            + practice_grid(s)
            + r"\vfill\centerline{\color{good}\bfseries \ding{51}\ Check your answers at the back. Fix any you got wrong.}"
            + "\n\\newpage\n")


def check_grid(s):
    h = s.get("check_h", "5.6cm")
    boxes = []
    for i, item in enumerate(s["check"], 1):
        it = norm(s, item)
        if it["type"] == "expr":
            boxes.append(rf"\cbox{{{i}}}{{{qtex(it['q'], compact=True)}}}{{{h}}}")
        else:
            span = CHECK_SPAN.get(it["type"], 2)
            opt = f"[raster multicolumn={span}]" if span > 1 else ""
            boxes.append(rf"\kbox{opt}{{{i}}}{{{h}}}{{{body(it, compact=True)}}}")
    return r"\begin{tcbraster}[raster columns=4, raster column skip=3mm]" "\n" + "\n".join(boxes) + "\n\\end{tcbraster}"


def skill_checks_page():
    """The Skill Checks, three skills per page, at the back so they can be torn out and marked."""
    total = sum(len(s["check"]) for s in C.SECTIONS)
    per_page = 3
    pages = [C.SECTIONS[i:i + per_page] for i in range(0, len(C.SECTIONS), per_page)]
    out = []
    for n, secs in enumerate(pages):
        last = n == len(pages) - 1
        label = "Teacher marks" if n == 0 else "Continued"
        right = (r"\fcolorbox{checkcol}{white}{\parbox[c][8mm][c]{4.2cm}{\centering\color{checkcol}\bfseries\large"
                 rf" Total: \underline{{\hspace{{9mm}}}} / {total}}}}}" if last else "")
        parts = [rf"\banner{{\ding{{51}}}}{{Skill Checks}}{{{label}}}{{checkcol}}",
                 r"{\large Name: \fillline{8cm}}\hfill" + right + r"\par\vspace{1mm}",
                 r"Do these \textbf{on your own --- no notes}. Show your working, and write your final answer on the line."]
        for s in secs:
            parts.append(rf"\checkhead{{{s['num']}}}{{{s['title']}}}{{{s['check_instr']}}}{{{len(s['check'])}}}")
            parts.append(check_grid(s))
        out.append("\n".join(parts) + "\n\\newpage\n")
    return "".join(out)


def answer_block(title, items, start=1):
    lis = "\n".join(rf"\item {m(a)}" for _q, a in items)
    return (rf"\textbf{{\color{{muted}}{title}}}" "\n"
            r"\begin{multicols}{4}\begin{enumerate}[nosep, label=\arabic*., start=" + str(start) + "]\n"
            + lis + "\n\\end{enumerate}\\end{multicols}\n")


def answer_tex(it):
    t = it["type"]
    if t == "word":
        return m(it["eq"]) + ", so " + m(it["sol"])
    if t == "written":
        return rich(it["a"])
    if t == "ineq":
        _v, op, val = split_rel(it["a"])
        b = int(float(val))
        return m(it["a"]) + r"\quad " + numline(b - 4, b + 4, 5.0, b, op, step=2)
    return m(it["a"])


def section_answers(s):
    items = [norm(s, it) for it in s["practice"]]
    if all(it["type"] == "expr" for it in items):
        return answer_block("", [(it["q"], it["a"]) for it in items])
    # consecutive runs of the same layout: short answers 4 across, number lines 2 across, sentences full width
    layout = {"written": 1, "word": 1, "ineq": 2}
    out, i = [], 0
    while i < len(items):
        cols = layout.get(items[i]["type"], 4)
        j = i
        while j < len(items) and layout.get(items[j]["type"], 4) == cols:
            j += 1
        lis = "\n".join(rf"\item {answer_tex(it)}" for it in items[i:j])
        lst = (r"\begin{enumerate}[nosep, label=\arabic*., start=" + str(i + 1) + "]\n" + lis + "\n\\end{enumerate}")
        out.append(lst if cols == 1 else rf"\begin{{multicols}}{{{cols}}}" + lst + r"\end{multicols}")
        i = j
    return "\n".join(out) + "\n"


def answers():
    out = [r"\setlength{\multicolsep}{3pt plus 1pt}\titlespacing*{\subsection}{0pt}{6pt}{2pt}",
           r"{\LARGE\bfseries\color{accent} Answers to the Practice Questions}\par\vspace{1mm}",
           r"{\small\color{muted} Terms can be in a different order and still be right --- e.g. "
           + m("2b + 3a") + " is the same as " + m("3a + 2b") + ".}\\par"]
    for s in C.SECTIONS:
        out.append(rf"\subsection*{{{s['num']}. {s['title']}}}")
        out.append(section_answers(s))
    return "\n".join(out)


def document(module):
    pre = PREAMBLE.replace("@@TITLE@@", C.TITLE).replace("@@MODULE@@", module)
    parts = [pre, cover()]
    for s in C.SECTIONS:
        parts += [learn_page(s), practice_page(s)]
    parts += [skill_checks_page(), answers(), "\n\\end{document}\n"]
    return "".join(parts)


def build(name):
    global C
    cfg = BOOKLETS[name]
    C = importlib.import_module(cfg["module"])
    tex_name, pdf_out = cfg["tex"], os.path.join(ROOT, cfg["pdf"])
    print(f"== {C.TITLE}")

    n, errors = check_all()
    if errors:
        print("ANSWER CHECK FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"Checked {n} practice answers: all correct (and simplified / fully factorised where that applies).")

    os.makedirs(TEX_DIR, exist_ok=True)
    tex_path = os.path.join(TEX_DIR, tex_name + ".tex")
    with open(tex_path, "w") as f:
        f.write(document(cfg["module"]))
    print("Wrote", os.path.relpath(tex_path, ROOT))

    if "--tex-only" in sys.argv:
        return
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name + ".tex"],
                           cwd=TEX_DIR, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            sys.exit("pdflatex failed")
    shutil.copy(os.path.join(TEX_DIR, tex_name + ".pdf"), pdf_out)
    log = open(os.path.join(TEX_DIR, tex_name + ".log"), errors="replace").read()
    warn = [l for l in log.splitlines() if "Overfull" in l or "LaTeX Warning" in l]
    print("Wrote", os.path.relpath(pdf_out, ROOT), f"({len(warn)} LaTeX warnings)")
    for w in warn[:15]:
        print("   ", w)


def main():
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOOKLETS)
    for name in names:
        build(name)


if __name__ == "__main__":
    main()

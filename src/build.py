#!/usr/bin/env python3
"""Build the booklet:  python3 src/build.py

1. Checks every practice answer in content.py: it must equal its question
   (tested at many random values), be simplified, and be fully factorised
   where that applies. Any problem stops the build.
2. Writes booklet/algebra-basic-skills.tex from content.py.
3. Runs pdflatex (twice) to make Algebra-Basic-Skills-Booklet.pdf.
"""
import math
import os
import random
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX_DIR = os.path.join(ROOT, "booklet")
TEX_NAME = "algebra-basic-skills"
PDF_OUT = os.path.join(ROOT, "Algebra-Basic-Skills-Booklet.pdf")

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
    mo = re.fullmatch(r"(-?\d*[a-z]?)\((.*)\)", a.replace(" ", ""))
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


def check_all():
    errors, count = [], 0

    def check(where, q, a, kind):
        nonlocal count
        count += 1
        if kind == "substitute":
            expr, env = split_sub(q)
            if not math.isclose(eval(to_python(expr), {}, env), float(a)):
                errors.append(f"{where}: '{q}' does NOT equal {a}")
            return
        if not same(q, a):
            errors.append(f"{where}: '{q}' is NOT equal to '{a}'")
        for p in (check_factorised(a) if kind == "factorise" else check_simplified(a)):
            errors.append(f"{where}: '{q}' -> '{a}': {p}")

    for s in C.SECTIONS:
        for i, (q, a) in enumerate(s["practice"], 1):
            check(f"Section {s['num']} practice Q{i}", q, a, s["kind"])
        for i, q in enumerate(s["check"], 1):
            if s["kind"] == "substitute":
                expr, env = split_sub(q)
                eval(to_python(expr), {}, env)  # must parse and have a value for every letter
            else:
                to_python(q)  # skill check questions must at least parse
            if not isinstance(q, str):
                errors.append(f"Section {s['num']} skill check Q{i}: must be a question only (no answer)")
    return count, errors


# ---------------------------------------------------------------------------
# LaTeX rendering
# ---------------------------------------------------------------------------

def mbody(expr):
    s = expr.replace("×", r"\times ").replace("÷", r"\div ")
    return re.sub(r"\^(\d+)", r"^{\1}", s)


def m(expr):
    return f"${mbody(expr)}$"


def qtex(q, compact=False):
    """A question for a box. Substitution questions also show their values."""
    if "|" not in q:
        return m(q)
    expr, vals = (x.strip() for x in q.split("|"))
    vals = m(vals.replace(",", ",\\ "))
    if compact:
        return m(expr) + r"\\[1pt]{\normalsize when " + vals + "}"
    return m(expr) + r"\enspace{\large when " + vals + "}"


def rich(text):
    """Convert \\example{q}{steps}{ans} lines and `maths` in LaTeX notes."""
    def ex(mo):
        return r"\example{%s}{%s}{%s}" % (qtex(mo.group(1), compact=True), mo.group(2), m("= " + mo.group(3)))
    text = re.sub(r"^\\example\{([^{}]*)\}\{(.*)\}\{([^{}]*)\}$", ex, text, flags=re.M)
    return re.sub(r"`([^`]+)`", lambda mo: m(mo.group(1)), text)


PREAMBLE = r"""% ------------------------------------------------------------------
% Algebra Basic Skills booklet.
% GENERATED by src/build.py from src/content.py -- edit content.py and
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
\fancyfoot[L]{\footnotesize\color{muted}Algebra Basic Skills}
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

\begin{document}
"""


def cover():
    rows = "\n".join(
        rf"\textbf{{\color{{accent}}\large {s['num']}}} & \textbf{{{s['title']}}}\newline "
        rf"{{\small\color{{muted}}{rich(s['can'])}}} & \tickbox & \hfill/\,{len(s['check'])} \\ \hline"
        for s in C.SECTIONS)
    total = sum(len(s["check"]) for s in C.SECTIONS)
    return rf"""
\thispagestyle{{empty}}
\begin{{tcolorbox}}[enhanced, colback=accent, colframe=accent, arc=3mm, halign=center, top=12mm, bottom=11mm]
\color{{white}}{{\small\bfseries B\,A\,S\,I\,C\quad S\,K\,I\,L\,L\,S\quad B\,O\,O\,K\,L\,E\,T}}\par\vspace{{3mm}}
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


def qgrid(items, cols, height):
    boxes = "\n".join(rf"\qbox{{{i}}}{{{qtex(q)}}}{{{height}}}" for i, (q, _a) in enumerate(items, 1))
    return (rf"\begin{{tcbraster}}[raster columns={cols}, raster column skip=4mm, raster row skip=3mm]"
            f"\n{boxes}\n\\end{{tcbraster}}\n")


def practice_page(s):
    return (rf"\banner{{{s['num']}}}{{{s['title']}}}{{Practice}}{{accent}}" "\n"
            rf"{{\large\textbf{{{s['instr']}}}}} {{\color{{muted}}Show your working in each box.}}\par\vspace{{1mm}}" "\n"
            + qgrid(s["practice"], 2, "3.45cm")
            + r"\vfill\centerline{\color{good}\bfseries \ding{51}\ Check your answers at the back. Fix any you got wrong.}"
            + "\n\\newpage\n")


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
            boxes = "\n".join(rf"\cbox{{{i}}}{{{qtex(q, compact=True)}}}{{5.6cm}}" for i, q in enumerate(s["check"], 1))
            parts.append(rf"\checkhead{{{s['num']}}}{{{s['title']}}}{{{s['check_instr']}}}{{{len(s['check'])}}}")
            parts.append(r"\begin{tcbraster}[raster columns=4, raster column skip=3mm]" "\n" + boxes + "\n\\end{tcbraster}")
        out.append("\n".join(parts) + "\n\\newpage\n")
    return "".join(out)


def answer_block(title, items, start=1):
    lis = "\n".join(rf"\item {m(a)}" for _q, a in items)
    return (rf"\textbf{{\color{{muted}}{title}}}" "\n"
            r"\begin{multicols}{4}\begin{enumerate}[nosep, label=\arabic*., start=" + str(start) + "]\n"
            + lis + "\n\\end{enumerate}\\end{multicols}\n")


def answers():
    out = [r"{\LARGE\bfseries\color{accent} Answers to the Practice Questions}\par\vspace{1mm}",
           r"{\small\color{muted} Terms can be in a different order and still be right --- e.g. "
           + m("2b + 3a") + " is the same as " + m("3a + 2b") + ".}\\par"]
    for s in C.SECTIONS:
        out.append(rf"\subsection*{{{s['num']}. {s['title']}}}")
        out.append(answer_block("", s["practice"]))
    return "\n".join(out)


def document():
    parts = [PREAMBLE, cover()]
    for s in C.SECTIONS:
        parts += [learn_page(s), practice_page(s)]
    parts += [skill_checks_page(), answers(), "\n\\end{document}\n"]
    return "".join(parts)


def main():
    n, errors = check_all()
    if errors:
        print("ANSWER CHECK FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"Checked {n} practice answers: all correct, simplified and fully factorised.")

    os.makedirs(TEX_DIR, exist_ok=True)
    tex_path = os.path.join(TEX_DIR, TEX_NAME + ".tex")
    with open(tex_path, "w") as f:
        f.write(document())
    print("Wrote", os.path.relpath(tex_path, ROOT))

    if "--tex-only" in sys.argv:
        return
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", TEX_NAME + ".tex"],
                           cwd=TEX_DIR, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            sys.exit("pdflatex failed")
    shutil.copy(os.path.join(TEX_DIR, TEX_NAME + ".pdf"), PDF_OUT)
    log = open(os.path.join(TEX_DIR, TEX_NAME + ".log"), errors="replace").read()
    warn = [l for l in log.splitlines() if "Overfull" in l or "LaTeX Warning" in l]
    print("Wrote", os.path.relpath(PDF_OUT, ROOT), f"({len(warn)} LaTeX warnings)")
    for w in warn[:15]:
        print("   ", w)


if __name__ == "__main__":
    main()

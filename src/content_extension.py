r"""Algebra Extension booklet: harder follow-up for students who did reasonably well.

Same conventions as content.py:
  - maths is plain text ("3x^2 - 2x", "2a × 3b", "x/2 + 1", "x <= 4");
    in the LaTeX notes put maths inside backticks.
  - practice items are checked by build.py before anything is written.
  - Skill Check items are questions ONLY: no answers are stored or printed.

Practice items are either (question, answer) pairs, checked using the
section's "kind", or dicts with a "type":
  solve   {"q": "3(x + 2) = 21", "a": "x = 5"}
  word    {"q": text, "eq": "5(n - 3) = 40", "sol": "n = 11"}
  written {"q": text, "a": model answer}            (an explanation, not auto-checked)
  ineq    {"q": "2x - 5 < 7", "a": "x < 6"}         (solve, then graph on a number line)
  table   {"x": [...], "y": [...], "a": "y = 2x + 3"}
  rule    {"q": text, "a": "C = 45h + 70", "pts": [(input, output), ...]}
"""

TITLE = "Algebra Extension"
SUBTITLE = "Take your algebra to the next level."
KICKER = "EXTENSION WORKBOOK"

# ---------------------------------------------------------------------------
# 1. Factorising fully
# ---------------------------------------------------------------------------
FACTORISE = {
    "id": "factorise",
    "num": 1,
    "title": "Factorising Fully",
    "can": "I can take out the highest common factor, e.g. `12x^2 + 30x = 6x(2x + 5)`",
    "kind": "factorise",
    "instr": "Factorise fully.",
    "check_instr": "Factorise fully.",
    "learn": r"""
\textbf{Factorising fully} means taking out the \textbf{highest common factor} (HCF):
the \textbf{biggest number} and \textbf{any letters} that go into every term.

\begin{tipbox}{The common mistake}
`12x + 36 = 6(2x + 6)` is \textbf{not} fully factorised --- look inside the bracket:
`2x` and `6` still have a common factor of 2. Taking out 12 straight away gives `12(x + 3)`.
\end{tipbox}

\begin{stepsbox}{How to factorise fully}
\begin{enumerate}[nosep]
\item \textbf{Numbers:} find the HCF. Try the \textbf{smaller} number first --- does it divide the other one? If not, try its next-biggest factor.
\item \textbf{Letters:} if \textbf{every} term has the same letter, take it out too (the lowest power).
\item \textbf{Divide} each term by the HCF and write the results in the bracket.
\item \textbf{Check:} nothing in the bracket shares a factor any more, and expanding gives the question.
\end{enumerate}
\end{stepsbox}

\subsection*{Worked examples}
\begin{examples}
\example{12x + 36}{12 goes into 36, so the HCF is 12\\`12x ÷ 12 = x`, `36 ÷ 12 = 3`}{12(x + 3)}
\example{18a - 24}{18 doesn't go into 24; 6 does\\`18a ÷ 6 = 3a`, `24 ÷ 6 = 4`}{6(3a - 4)}
\example{12x^2 + 30x}{Numbers: HCF is 6\\Letters: both have `x`}{6x(2x + 5)}
\example{8ab + 12a}{Numbers: HCF is 4\\Letters: both have `a`}{4a(2b + 3)}
\example{15x^2 - 25x}{Numbers: HCF is 5\\Letters: both have `x`}{5x(3x - 5)}
\example{14xy + 21y}{Numbers: HCF is 7\\Letters: both have `y`}{7y(2x + 3)}
\end{examples}

\begin{rememberbox}
`12x^2 + 30x = 6(2x^2 + 5x)` is only \textbf{partly} factorised: `2x^2` and `5x` both still have an `x`.
Always look inside your bracket before you stop.
\end{rememberbox}
""",
    "practice": [
        ("10x + 30", "10(x + 3)"),
        ("16a - 24", "8(2a - 3)"),
        ("18y + 27", "9(2y + 3)"),
        ("24x - 36", "12(2x - 3)"),
        ("20m + 50", "10(2m + 5)"),
        ("42 - 28x", "14(3 - 2x)"),
        ("x^2 + 9x", "x(x + 9)"),
        ("6x^2 + 9x", "3x(2x + 3)"),
        ("10a^2 - 15a", "5a(2a - 3)"),
        ("16x^2 + 24x", "8x(2x + 3)"),
        ("9ab + 12a", "3a(3b + 4)"),
        ("20xy - 30y", "10y(2x - 3)"),
    ],
    "check": [
        "15x + 45",
        "24a - 36",
        "8x^2 + 20x",
        "18xy - 12x",
    ],
    "check_h": "4.4cm",
}

# ---------------------------------------------------------------------------
# 2. Substituting negative numbers
# ---------------------------------------------------------------------------
SUBSTITUTE = {
    "id": "substitute",
    "num": 2,
    "title": "Substituting Negatives",
    "can": "I can substitute negative numbers, e.g. if `x = -3` then `x^2 - 2x = 15`",
    "kind": "substitute",
    "instr": "Find the value of each expression.",
    "check_instr": "Find the value.",
    "learn": r"""
When you substitute a \textbf{negative number}, always put it in \textbf{brackets}.
Then use the sign rules and BEDMAS.

\begin{center}
\renewcommand{\arraystretch}{1.35}
\begin{tabular}{|l|l|}
\hline
\rowcolor{accentlight}\textbf{Rule} & \textbf{Example} \\ \hline
Same signs multiply to a \textbf{positive} & `(-3) × (-4) = 12` \\ \hline
Different signs multiply to a \textbf{negative} & `5 × (-2) = -10` \\ \hline
Squaring a negative gives a \textbf{positive} & `(-6)^2 = (-6) × (-6) = 36` \\ \hline
Subtracting a negative means \textbf{add} & `7 - (-2) = 7 + 2 = 9` \\ \hline
\end{tabular}
\end{center}

\begin{tipbox}{Why the brackets matter}
If `x = -4`, then `x^2` means `(-4)^2 = 16`. Without brackets it is easy to write `-4^2` and get `-16` by mistake.
\end{tipbox}

\subsection*{Worked examples}
\begin{examples}
\example{2x + 5 | x = -3}{`2 × (-3) + 5`\\`= -6 + 5`}{-1}
\example{10 - 2x | x = -3}{`10 - 2 × (-3)`\\`= 10 - (-6) = 10 + 6`}{16}
\example{x^2 | x = -4}{`(-4) × (-4)`\\Same signs: positive}{16}
\example{ab | a = -3, b = -4}{`(-3) × (-4)`\\Same signs: positive}{12}
\example{3a - b | a = -2, b = -5}{`3 × (-2) - (-5)`\\`= -6 + 5`}{-1}
\example{x^2 - 2x | x = -3}{`(-3)^2 - 2 × (-3)`\\`= 9 + 6`}{15}
\end{examples}

\begin{rememberbox}
Write out every step with brackets. Most mistakes come from doing two sign changes in your head at once.
\end{rememberbox}
""",
    "practice": [
        ("x + 8 | x = -3", "5"),
        ("4x | x = -5", "-20"),
        ("7 - x | x = -2", "9"),
        ("3y + 10 | y = -4", "-2"),
        ("a^2 | a = -6", "36"),
        ("ab | a = -2, b = 7", "-14"),
        ("2a - b | a = 3, b = -4", "10"),
        ("5 - 2x | x = -3", "11"),
        ("x^2 + 3x | x = -2", "-2"),
        ("2x^2 | x = -3", "18"),
        ("ab - c | a = -2, b = -3, c = -5", "11"),
        ("3x^2 - 2x | x = -1", "5"),
    ],
    "check": [
        "5x + 3 | x = -2",
        "a - b | a = -4, b = -6",
        "x^2 - 4x | x = -3",
        "2ab | a = -5, b = 3",
    ],
    "check_h": "4.4cm",
}

# ---------------------------------------------------------------------------
# 3. Index laws
# ---------------------------------------------------------------------------
INDICES = {
    "id": "indices",
    "num": 3,
    "title": "Index Laws",
    "can": "I can use the index laws and explain them, e.g. `3^4 × 3^2 = 3^6`",
    "kind": "simplify",
    "instr": "Simplify, leaving your answer in index form.",
    "check_instr": "Simplify, and explain.",
    "learn": r"""
`3^4` means `3 × 3 × 3 × 3`. The 3 is the \textbf{base} and the 4 is the \textbf{index} (power).
The index laws only work when the \textbf{bases are the same}.

\begin{center}
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|l|c|l|}
\hline
\rowcolor{accentlight}\textbf{Law} & \textbf{Rule} & \textbf{Example} \\ \hline
Multiplying: \textbf{add} the indices & `a^m × a^n = a^{m+n}` & `x^5 × x^3 = x^8` \\ \hline
Dividing: \textbf{subtract} the indices & `a^m ÷ a^n = a^{m-n}` & `a^7 ÷ a^2 = a^5` \\ \hline
Power of a power: \textbf{multiply} the indices & `(a^m)^n = a^{mn}` & `(x^3)^2 = x^6` \\ \hline
\end{tabular}
\end{center}
The \textbf{base stays the same}. Numbers in front are multiplied or divided as normal: `4x^2 × 3x^5 = 12x^7`.

\begin{tcolorbox}[base, colframe=accent, colback=accentlight]
\textbf{Liam says that} `3^4 × 3^2 = 9^6` \textbf{because} `3 × 3 = 9` \textbf{and} `4 + 2 = 6`. \textbf{Explain why Liam is wrong.}\\[3pt]
\textbf{Answer:} When you multiply powers with the \textbf{same base}, you \textbf{keep the base} and \textbf{add the indices}: `a^m × a^n = a^{m+n}`.
Liam multiplied the bases, but the base should stay as 3.
`3^4 × 3^2 = (3 × 3 × 3 × 3) × (3 × 3)`, which is six 3s multiplied together, so the correct answer is `3^6` (`= 729`), not `9^6`.
\end{tcolorbox}

\subsection*{Worked examples}
\begin{examples}
\example{2x^3 × 5x^4}{Numbers: `2 × 5 = 10`\\Indices: `3 + 4 = 7`}{10x^7}
\example{15a^6 ÷ 3a^2}{Numbers: `15 ÷ 3 = 5`\\Indices: `6 - 2 = 4`}{5a^4}
\example{(2x^3)^2}{Everything in the bracket is squared\\`2^2 = 4`, `3 × 2 = 6`}{4x^6}
\end{examples}

\begin{rememberbox}
Watch out for these common mistakes:
\begin{itemize}[nosep]
\item `2x^3 × 5x^4` is `10x^7`, not `7x^7` --- the numbers in front are \textbf{multiplied}, only the indices are added.
\item `(2x^3)^2` is `4x^6`, not `2x^6` --- the 2 inside the bracket is squared too.
\item `x^6 ÷ x^2` is `x^4`, not `x^3` --- dividing powers means \textbf{subtract} the indices, not divide them.
\end{itemize}
\end{rememberbox}
""",
    "practice": [
        ("5^3 × 5^4", "5^7"),
        ("x^6 × x^2", "x^8"),
        ("7^9 ÷ 7^3", "7^6"),
        ("a^10 ÷ a^4", "a^6"),
        ("(x^4)^3", "x^12"),
        ("3x^2 × 4x^5", "12x^7"),
        ("20a^8 ÷ 5a^3", "4a^5"),
        ("(3x^2)^2", "9x^4"),
        {"type": "written",
         "q": r"Mia says `2^3 × 2^4 = 4^7` because `2 × 2 = 4` and `3 + 4 = 7`. "
              r"Explain why Mia is wrong. State the index law and give the correct answer.",
         "a": r"When multiplying powers with the same base, keep the base and add the indices: "
              r"`a^m × a^n = a^{m+n}`. The base stays 2, so `2^3 × 2^4 = 2^7` (`= 128`), not `4^7`."},
        {"type": "written",
         "q": r"Tane says `5^8 ÷ 5^2 = 1^4` because `5 ÷ 5 = 1` and `8 ÷ 2 = 4`. "
              r"Explain why Tane is wrong. State the index law and give the correct answer.",
         "a": r"When dividing powers with the same base, keep the base and subtract the indices: "
              r"`a^m ÷ a^n = a^{m-n}`. The base stays 5, so `5^8 ÷ 5^2 = 5^6`, not `1^4`."},
    ],
    "check": [
        "2^5 × 2^3",
        "12x^7 ÷ 3x^2",
        {"type": "written",
         "q": r"Ana says `4^3 × 4^5 = 16^8` because `4 × 4 = 16` and `3 + 5 = 8`. "
              r"Explain why Ana is wrong. State the index law and give the correct answer."},
    ],
    "check_h": "5.7cm",
}

# ---------------------------------------------------------------------------
# 4. Equations with brackets, and writing equations
# ---------------------------------------------------------------------------
EQUATIONS = {
    "id": "equations",
    "num": 4,
    "title": "Equations with Brackets",
    "can": "I can solve equations like `3(x + 4) = 27`, and write equations from a story",
    "kind": "solve",
    "instr": "Solve each equation. For the stories, write an equation and then solve it.",
    "check_instr": "Solve.",
    "learn": r"""
\textbf{Method 1 --- expand first.} Expand the bracket, then solve the two-step equation.\\
\textbf{Method 2 --- divide first.} If the number outside divides the other side exactly, divide first.

\begin{examples}
\example{3(x + 4) = 27}{Expand: `3x + 12 = 27`\\`3x = 15`}{x = 5}
\example{3(x + 4) = 27}{Divide by 3: `x + 4 = 9`\\Take 4 from both sides}{x = 5}
\example{2(3x - 1) = 19}{Expand: `6x - 2 = 19`\\`6x = 21`}{x = 3.5}
\end{examples}
\textbf{Check} by substituting your answer back in: `3(5 + 4) = 3 × 9 = 27` \cmark

\subsection*{Writing equations from a story}
\begin{stepsbox}{Turn words into an equation}
\begin{enumerate}[nosep]
\item Choose a \textbf{letter} for the unknown (say what it stands for).
\item Follow the story \textbf{in order}. Use \textbf{brackets} when something happens to a whole amount: \textquotedblleft add 5, \textbf{then} multiply by 4\textquotedblright{} is `4(n + 5)`.
\item Make it \textbf{equal} to the total, then \textbf{solve}.
\end{enumerate}
\end{stepsbox}

\begin{examples}
\example{\text{Sione's number}}{Thinks of a number `n`, adds 5, then multiplies by 4. The answer is 36.\\`4(n + 5) = 36`}{n = 4}
\example{\text{Rectangle}}{Width 5 cm, length `(x + 3)` cm, area 45 cm².\\`5(x + 3) = 45`}{x = 6}
\example{\text{Pizza}}{3 friends each buy a pizza (\$`p`) and a \$4 drink. Total \$45.\\`3(p + 4) = 45`}{p = 11}
\end{examples}
""",
    "practice": [
        {"type": "solve", "q": "2(x + 3) = 14", "a": "x = 4"},
        {"type": "solve", "q": "5(x - 2) = 35", "a": "x = 9"},
        {"type": "solve", "q": "4(2x + 1) = 36", "a": "x = 4"},
        {"type": "solve", "q": "3(x + 5) = 6", "a": "x = -3"},
        {"type": "solve", "q": "6(x - 4) = -12", "a": "x = 2"},
        {"type": "solve", "q": "2(3x - 1) = 19", "a": "x = 3.5"},
        {"type": "word",
         "q": "Aroha thinks of a number, subtracts 3, then multiplies the result by 5. The answer is 40. "
              "Write an equation and solve it to find her number.",
         "eq": "5(n - 3) = 40", "sol": "n = 11"},
        {"type": "word",
         "q": "A rectangle is 4 cm wide and $(x + 6)$ cm long. Its area is 52 cm². "
              "Write an equation and solve it to find $x$.",
         "eq": "4(x + 6) = 52", "sol": "x = 7"},
        {"type": "word",
         "q": r"Five students each buy a movie ticket costing \$$t$ and a \$3 popcorn. They spend \$85 altogether. "
              "Write an equation and solve it to find the cost of a ticket.",
         "eq": "5(t + 3) = 85", "sol": "t = 14"},
    ],
    "check": [
        {"type": "solve", "q": "3(x - 4) = 18"},
        {"type": "solve", "q": "4(2x + 3) = 4"},
        {"type": "word",
         "q": "Tama thinks of a number, adds 7, then multiplies by 3. The answer is 39. "
              "Write an equation and solve it."},
    ],
    "check_h": "5.6cm",
}

# ---------------------------------------------------------------------------
# 5. Inequalities
# ---------------------------------------------------------------------------
INEQUALITIES = {
    "id": "inequalities",
    "num": 5,
    "title": "Inequalities",
    "can": "I can solve an inequality and show it on a number line, e.g. `2x + 3 < 11` gives `x < 4`",
    "kind": "ineq",
    "instr": "Solve each inequality, then show the answer on the number line.",
    "check_instr": "Solve, then show on the number line.",
    "learn": r"""
\begin{center}
\renewcommand{\arraystretch}{1.35}
\begin{tabular}{|c|l|c|}
\hline
\rowcolor{accentlight}\textbf{Symbol} & \textbf{Meaning} & \textbf{Circle on the number line} \\ \hline
`<` & less than & open \tikz\draw[accent,thick,fill=white] (0,0) circle (1.1mm); \\ \hline
`>` & greater than & open \tikz\draw[accent,thick,fill=white] (0,0) circle (1.1mm); \\ \hline
`<=` & less than \textbf{or equal to} & filled \tikz\filldraw[accent,thick] (0,0) circle (1.1mm); \\ \hline
`>=` & greater than \textbf{or equal to} & filled \tikz\filldraw[accent,thick] (0,0) circle (1.1mm); \\ \hline
\end{tabular}
\end{center}
The \textbf{open} circle means the number itself is \textbf{not} included; \textbf{filled} means it is.
The arrow points the way the numbers go: \textbf{left} for less than, \textbf{right} for greater than.

\begin{stepsbox}{How to solve an inequality}
Solve it \textbf{exactly like an equation}, with one extra rule:
if you \textbf{multiply or divide by a negative number}, \textbf{flip the inequality sign}.
\end{stepsbox}

\subsection*{Worked examples}
\textbf{1.} `2x + 3 < 11` \quad $\Rightarrow$ \quad `2x < 8` \quad $\Rightarrow$ \quad `x < 4` \quad (open circle, arrow left)\par
\hspace*{6mm}@@numline -3 9 4 < 11@@\par\vspace{2mm}

\textbf{2.} `3(x - 1) >= 6` \quad $\Rightarrow$ \quad `x - 1 >= 2` \quad $\Rightarrow$ \quad `x >= 3` \quad (filled circle, arrow right)\par
\hspace*{6mm}@@numline -3 9 3 >= 11@@\par\vspace{2mm}

\textbf{3.} `5 - 2x <= 11` \quad $\Rightarrow$ \quad `-2x <= 6` \quad $\Rightarrow$ \quad `x >= -3` \quad (divided by `-2`, so \textbf{flip}!)\par
\hspace*{6mm}@@numline -9 3 -3 >= 11@@

\begin{rememberbox}
Check with a test number. For `x >= -3`, try `x = 0`: `5 - 2 × 0 = 5`, and `5 <= 11` \cmark.
So numbers bigger than `-3` work, and the arrow points right.
\end{rememberbox}
""",
    "practice": [
        {"type": "ineq", "q": "x + 4 > 7", "a": "x > 3"},
        {"type": "ineq", "q": "3x <= 12", "a": "x <= 4"},
        {"type": "ineq", "q": "2x - 5 < 7", "a": "x < 6"},
        {"type": "ineq", "q": "4x + 3 >= -9", "a": "x >= -3"},
        {"type": "ineq", "q": "x/2 + 1 > 3", "a": "x > 4"},
        {"type": "ineq", "q": "3(x - 2) <= 9", "a": "x <= 5"},
        {"type": "ineq", "q": "5 - x < 2", "a": "x > 3"},
        {"type": "ineq", "q": "-2x + 1 >= 7", "a": "x <= -3"},
    ],
    "check": [
        {"type": "ineq", "q": "3x - 4 > 8"},
        {"type": "ineq", "q": "6 - 2x <= 10"},
    ],
    "check_h": "5.6cm",
}

# ---------------------------------------------------------------------------
# 6. Linear rules from tables and stories
# ---------------------------------------------------------------------------
LINEAR = {
    "id": "linear",
    "num": 6,
    "title": "Writing Linear Rules",
    "can": "I can write a rule like `y = 2x + 3` from a table of values or a story",
    "kind": "table",
    "instr": "Write the rule for each table. For the stories, write an equation.",
    "check_instr": "Write the rule.",
    "learn": r"""
A linear rule looks like `y = mx + c`.
\begin{itemize}[nosep]
\item `m` is how much `y` \textbf{changes} each time `x` goes up by 1 (the \textbf{difference}).
\item `c` is the value of `y` when `x = 0` (the \textbf{starting value}).
\end{itemize}

\begin{stepsbox}{From a table}
\begin{enumerate}[nosep]
\item Check `x` goes up by 1 each time. Find the \textbf{difference} between the `y` values: that's `m`.
\item Find `y` when `x = 0`: that's `c`. If the table doesn't start at 0, \textbf{work backwards} one step at a time.
\item Write `y = mx + c` and \textbf{check} it with another column.
\end{enumerate}
\end{stepsbox}

\begin{examples}
\example{\begin{tabular}{c|cccc}$x$&0&1&2&3\\\hline$y$&3&5&7&9\end{tabular}}{Goes up by 2: `m = 2`\\At `x = 0`, `y = 3`: `c = 3`}{y = 2x + 3}
\example{\begin{tabular}{c|cccc}$x$&1&2&3&4\\\hline$y$&7&10&13&16\end{tabular}}{Goes up by 3: `m = 3`\\Back one step: `7 - 3 = 4`}{y = 3x + 4}
\example{\begin{tabular}{c|cccc}$x$&0&1&2&3\\\hline$y$&10&8&6&4\end{tabular}}{Goes \textbf{down} by 2: `m = -2`\\At `x = 0`, `y = 10`}{y = -2x + 10}
\end{examples}

\subsection*{From a story}
The \textbf{fixed amount} (a starting fee or starting value) is `c`. The amount \textbf{per} hour, week, km\ldots{} is `m`.
\begin{examples}
\example{\text{Gym}}{\$60 joining fee plus \$15 per week. Cost `C` after `w` weeks.}{C = 15w + 60}
\example{\text{Candle}}{30 cm tall, burns down 2 cm every hour. Height `h` after `t` hours.}{h = 30 - 2t}
\example{\text{Phone}}{\$20 a month plus \$5 per GB of data. Cost `C` for `g` GB.}{C = 5g + 20}
\end{examples}
""",
    "practice": [
        {"type": "table", "x": [0, 1, 2, 3], "y": [1, 4, 7, 10], "a": "y = 3x + 1"},
        {"type": "table", "x": [0, 1, 2, 3], "y": [5, 7, 9, 11], "a": "y = 2x + 5"},
        {"type": "table", "x": [1, 2, 3, 4], "y": [6, 10, 14, 18], "a": "y = 4x + 2"},
        {"type": "table", "x": [1, 2, 3, 4], "y": [2, 7, 12, 17], "a": "y = 5x - 3"},
        {"type": "table", "x": [0, 1, 2, 3], "y": [12, 9, 6, 3], "a": "y = -3x + 12"},
        {"type": "table", "x": [2, 3, 4, 5], "y": [1, 3, 5, 7], "a": "y = 2x - 3"},
        {"type": "rule",
         "q": r"An electrician charges a \$70 call-out fee plus \$45 per hour. "
              r"Write an equation for the total cost $C$ of a job that takes $h$ hours.",
         "a": "C = 45h + 70", "pts": [(0, 70), (1, 115), (3, 205)]},
        {"type": "rule",
         "q": r"A taxi charges \$3.50 to start, plus \$2 per kilometre. "
              r"Write an equation for the fare $F$ for a trip of $d$ kilometres.",
         "a": "F = 2d + 3.5", "pts": [(0, 3.5), (1, 5.5), (10, 23.5)]},
        {"type": "rule",
         "q": "A water tank holds 200 litres and leaks 5 litres every hour. "
              "Write an equation for the amount of water $W$ left after $t$ hours.",
         "a": "W = 200 - 5t", "pts": [(0, 200), (1, 195), (4, 180)]},
    ],
    "check": [
        {"type": "table", "x": [1, 2, 3, 4], "y": [1, 4, 7, 10]},
        {"type": "rule",
         "q": r"A school trip costs \$200 for the bus plus \$12 per student. "
              r"Write an equation for the total cost $C$ when $n$ students go."},
    ],
    "check_h": "5.6cm",
}

SECTIONS = [FACTORISE, SUBSTITUTE, INDICES, EQUATIONS, INEQUALITIES, LINEAR]

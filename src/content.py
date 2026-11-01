r"""All booklet content: learning notes, practice questions, skill checks.

Maths is written as plain text, e.g. "3x^2 - 2x", "2a × 3b", "12x ÷ 4".
In the LaTeX notes (the "learn" strings) put maths inside backticks:
`3a + 4a = 7a`. build.py turns both into LaTeX maths.

Practice questions are (question, answer) pairs. build.py checks every
answer is equal to its question, simplified, and (for factorising) fully
factorised, before it writes the booklet.

Skill Check questions are questions ONLY. Their answers are deliberately
not stored or printed anywhere: the teacher marks them.
"""

TITLE = "Algebra Basic Skills"
SUBTITLE = "Learn it. Practise it. Show you can do it."

# ---------------------------------------------------------------------------
# 1. Collecting like terms
# ---------------------------------------------------------------------------
LIKE_TERMS = {
    "id": "like-terms",
    "num": 1,
    "title": "Collecting Like Terms",
    "can": "I can add and subtract like terms, e.g. `3a + 4a = 7a`",
    "kind": "simplify",
    "instr": "Simplify by collecting like terms.",
    "check_instr": "Simplify by collecting like terms.",
    "learn": r"""
\textbf{Like terms} have \textbf{exactly the same letter part}. You can only add or
subtract like terms.

\medskip
\begin{center}
\renewcommand{\arraystretch}{1.35}
\begin{tabular}{|l|l|}
\hline
\rowcolor{accentlight}\textbf{Like terms \cmark} & \textbf{NOT like terms \xmark} \\ \hline
`3a` and `5a` & `3a` and `5b` \quad (different letters) \\ \hline
`x` and `7x` & `x` and `7` \quad (one has no letter) \\ \hline
`2x^2` and `x^2` & `x^2` and `x` \quad (`x^2` is not the same as `x`) \\ \hline
`4ab` and `ab` & `ab` and `a` \\ \hline
\end{tabular}
\end{center}

\begin{tipbox}{Think of the letters as objects}
3 apples + 4 apples = 7 apples, so `3a + 4a = 7a`.\\
But 3 apples + 2 bananas can't be joined, so `3a + 2b` stays as `3a + 2b`.
\end{tipbox}

\begin{tipbox}{A letter on its own means 1 of it}
`a` is the same as `1a`. So `a + a + a = 3a`.
\end{tipbox}

\subsection*{Worked examples}
\begin{examples}
\example{3a + 4a}{3 lots of `a` plus 4 lots of `a`}{7a}
\example{6x - 2x}{6 take away 2 is 4}{4x}
\example{5y - y}{`y` means `1y`, and `5 - 1 = 4`}{4y}
\example{2a + 3b + 4a + b}{The `a`'s: `2a + 4a = 6a`\\The `b`'s: `3b + b = 4b`}{6a + 4b}
\example{x^2 + 3x + 2x^2}{The `x^2`'s: `x^2 + 2x^2 = 3x^2`\\The `x`'s: just `3x`}{3x^2 + 3x}
\example{7m + 2 - 3m}{The `m`'s: `7m - 3m = 4m`\\The numbers: just `2`}{4m + 2}
\end{examples}

\begin{rememberbox}
The sign ($+$ or $-$) in \textbf{front} of a term belongs to that term.
Circle or highlight each type of term in a different colour before you add them up.
\end{rememberbox}
""",
    "practice": [
        ("a + a + a", "3a"),
        ("2a + 3a", "5a"),
        ("7b - 3b", "4b"),
        ("6y - y", "5y"),
        ("2p + 3p + p", "6p"),
        ("3x^2 + 4x^2", "7x^2"),
        ("2a + 3b + 4a", "6a + 3b"),
        ("5x + 2y + x", "6x + 2y"),
        ("4x + 3 + 2x", "6x + 3"),
        ("5a + 2b - 3a", "2a + 2b"),
        ("x^2 + 2x + 3x", "x^2 + 5x"),
        ("2x^2 + x + x^2", "3x^2 + x"),
    ],
    "check": [
        "5a + 2a",
        "8x - 3x",
        "4a + 3b + 2a",
        "x^2 + 5x + 2x^2",
    ],
}

# ---------------------------------------------------------------------------
# 2. Multiplying
# ---------------------------------------------------------------------------
MULTIPLY = {
    "id": "multiply",
    "num": 2,
    "title": "Multiplying Algebra",
    "can": r"I can multiply terms, e.g. `2a × 3b = 6ab` and `x × x = x^2`",
    "kind": "simplify",
    "instr": "Simplify.",
    "check_instr": "Simplify.",
    "learn": r"""
In algebra we \textbf{don't write the $\times$ sign}. Letters and numbers that are multiplied
are written next to each other, \textbf{number first}.

\medskip
\begin{center}
\renewcommand{\arraystretch}{1.35}
\begin{tabular}{|c|l|}
\hline
\rowcolor{accentlight}\textbf{We write\ldots} & \textbf{\ldots it means} \\ \hline
`3a` & `3 × a` \\ \hline
`ab` & `a × b` \\ \hline
`5xy` & `5 × x × y` \\ \hline
`x^2` & `x × x` \quad (say \textquotedblleft{}$x$ squared'') \\ \hline
\end{tabular}
\end{center}

\begin{stepsbox}{How to multiply terms}
\begin{enumerate}[nosep]
\item \textbf{Multiply the numbers} together.
\item \textbf{Write the letters} after the number, in alphabetical order.
\item If the \textbf{same letter} appears twice, write it as a \textbf{square}: `x × x = x^2`.
\end{enumerate}
\end{stepsbox}

\subsection*{Worked examples}
\begin{examples}
\example{4 × a}{Number first, then the letter}{4a}
\example{a × b}{Write the letters together}{ab}
\example{2a × 4}{Numbers: `2 × 4 = 8`\\Letters: `a`}{8a}
\example{2a × 3b}{Numbers: `2 × 3 = 6`\\Letters: `a` and `b`}{6ab}
\example{x × x}{The same letter twice is \textquotedblleft{}squared''}{x^2}
\example{3x × 2x}{Numbers: `3 × 2 = 6`\\Letters: `x × x = x^2`}{6x^2}
\end{examples}

\begin{rememberbox}
When you \textbf{multiply}, the numbers multiply (`3 × 2 = 6`) --- don't add them!
And `x × x` is `x^2`, not `2x`.\\[2pt]
\textbf{Going further:} `x × x × x = x^3` (\textquotedblleft{}$x$ cubed''), and `x^2 × x = x^3`.
\end{rememberbox}
""",
    "practice": [
        ("4 × a", "4a"),
        ("a × b", "ab"),
        ("2 × 3a", "6a"),
        ("3x × 4", "12x"),
        ("a × a", "a^2"),
        ("2a × b", "2ab"),
        ("2a × 3b", "6ab"),
        ("4x × 2y", "8xy"),
        ("3a × a", "3a^2"),
        ("2x × 5x", "10x^2"),
        ("4m × 3m", "12m^2"),
        ("x × x × x", "x^3"),
    ],
    "check": [
        "3 × 5a",
        "2a × 4b",
        "x × x",
        "3x × 2x",
    ],
}

# ---------------------------------------------------------------------------
# 3. Dividing
# ---------------------------------------------------------------------------
DIVIDE = {
    "id": "divide",
    "num": 3,
    "title": "Dividing Algebra",
    "can": "I can divide terms, e.g. `8x ÷ 2 = 4x` and `6ab ÷ 2a = 3b`",
    "kind": "simplify",
    "instr": "Simplify.",
    "check_instr": "Simplify.",
    "learn": r"""
Dividing is the opposite of multiplying. A division can also be written as a fraction:
`6a ÷ 2` is the same as $\dfrac{6a}{2}$.

\begin{stepsbox}{How to divide terms}
\begin{enumerate}[nosep]
\item \textbf{Divide the numbers.}
\item \textbf{Cancel any letter} that is on the top \textbf{and} the bottom.
\item Write down what is left.
\end{enumerate}
\end{stepsbox}

\begin{tipbox}{Why can letters cancel?}
Anything divided by itself is 1. Just like `5 ÷ 5 = 1`, `a ÷ a = 1`.
So $\dfrac{ab}{a} = b$.
\end{tipbox}

\subsection*{Worked examples}
\begin{examples}
\example{6a ÷ 2}{Numbers: `6 ÷ 2 = 3`\\Letters: `a` stays}{3a}
\example{ab ÷ a}{The `a` cancels\\`b` is left}{b}
\example{8x ÷ x}{The `x` cancels\\`8` is left}{8}
\example{12ab ÷ 4a}{Numbers: `12 ÷ 4 = 3`\\`a` cancels, `b` is left}{3b}
\example{x^2 ÷ x}{`x^2` is `x × x`\\One `x` cancels, one is left}{x}
\example{6x^2 ÷ 3x}{Numbers: `6 ÷ 3 = 2`\\Letters: `x^2 ÷ x = x`}{2x}
\end{examples}

\begin{rememberbox}
If \textbf{all} the letters cancel, you are left with just a number, e.g. `5a ÷ a = 5`.
Write `x^2` as `x × x` if it helps you see what cancels.
\end{rememberbox}
""",
    "practice": [
        ("8a ÷ 2", "4a"),
        ("12x ÷ 3", "4x"),
        ("20y ÷ 4", "5y"),
        ("6m ÷ 6", "m"),
        ("ab ÷ b", "a"),
        ("5a ÷ a", "5"),
        ("6ab ÷ 2a", "3b"),
        ("12xy ÷ 4y", "3x"),
        ("x^2 ÷ x", "x"),
        ("4x^2 ÷ x", "4x"),
        ("6x^2 ÷ 2x", "3x"),
        ("15a^2 ÷ 5a", "3a"),
    ],
    "check": [
        "12x ÷ 4",
        "ab ÷ b",
        "10ab ÷ 5a",
        "8x^2 ÷ 2x",
    ],
}

# ---------------------------------------------------------------------------
# 4. Expanding brackets (single brackets only, including negatives)
# ---------------------------------------------------------------------------
EXPAND = {
    "id": "expand",
    "num": 4,
    "title": "Expanding Brackets",
    "can": "I can expand brackets, e.g. `3(x + 2) = 3x + 6` and `-2(x - 4) = -2x + 8`",
    "kind": "simplify",
    "instr": "Expand. Be careful with the negative signs!",
    "check_instr": "Expand.",
    "learn": r"""
\textbf{Expanding} means getting rid of the brackets by multiplying.
A number or letter right in front of a bracket means \textbf{multiply everything inside}
the bracket by it.

\begin{stepsbox}{Multiply the outside by EVERY term inside}
Draw arrows so you don't miss one:
\[ 3(x + 2) \;\;\longrightarrow\;\; 3 \times x \;\text{ and }\; 3 \times 2 \;\;\longrightarrow\;\; 3x + 6 \]
\end{stepsbox}

\subsection*{Worked examples}
\begin{examples}
\example{4(a + 5)}{`4 × a = 4a`\\`4 × 5 = 20`}{4a + 20}
\example{2(x - 3)}{`2 × x = 2x`\\`2 × (-3) = -6`}{2x - 6}
\example{x(x + 5)}{`x × x = x^2`\\`x × 5 = 5x`}{x^2 + 5x}
\end{examples}

\subsection*{Negative numbers outside the bracket}
When the number outside is \textbf{negative}, use the sign rules:
\begin{center}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{|c|c|}
\hline
\rowcolor{accentlight} \textbf{Signs} & \textbf{Answer} \\ \hline
same signs: \; $+ \times +$ \; or \; $- \times -$ & \textbf{positive} $(+)$ \\ \hline
different signs: \; $+ \times -$ \; or \; $- \times +$ & \textbf{negative} $(-)$ \\ \hline
\end{tabular}
\end{center}

\begin{examples}
\example{-2(x + 3)}{`-2 × x = -2x`\\`-2 × 3 = -6`}{-2x - 6}
\example{-3(x - 4)}{`-3 × x = -3x`\\`-3 × (-4) = +12`}{-3x + 12}
\example{-(x - 5)}{A minus on its own means `-1`\\`-1 × x = -x`,\; `-1 × (-5) = +5`}{-x + 5}
\end{examples}

\begin{rememberbox}
The outside term multiplies \textbf{every} term inside: `3(x + 2)` is `3x + 6`, \textbf{not} `3x + 2`.
With a negative outside, \textbf{every sign inside changes}: `-2(x - 4) = -2x + 8`.
\end{rememberbox}
""",
    "practice": [
        ("2(x + 3)", "2x + 6"),
        ("3(a + 4)", "3a + 12"),
        ("4(y - 2)", "4y - 8"),
        ("3(2x + 1)", "6x + 3"),
        ("x(x + 2)", "x^2 + 2x"),
        ("x(x - 3)", "x^2 - 3x"),
        ("-2(x + 3)", "-2x - 6"),
        ("-4(x - 2)", "-4x + 8"),
        ("-(x + 7)", "-x - 7"),
        ("2(3 - x)", "6 - 2x"),
        ("-2(3x - 1)", "-6x + 2"),
        ("-x(x + 2)", "-x^2 - 2x"),
    ],
    "check": [
        "3(x + 5)",
        "2(4a - 3)",
        "x(x - 2)",
        "-4(x - 3)",
    ],
}

# ---------------------------------------------------------------------------
# 5. Factorising (single brackets only, including negatives)
# ---------------------------------------------------------------------------
FACTORISE = {
    "id": "factorise",
    "num": 5,
    "title": "Factorising into Brackets",
    "can": "I can factorise, e.g. `2x + 6 = 2(x + 3)`",
    "kind": "factorise",
    "instr": "Factorise fully.",
    "check_instr": "Factorise fully.",
    "learn": r"""
\textbf{Factorising} is the \textbf{opposite of expanding}. We put the brackets back in.
\begin{center}
\colorbox{accentlight}{\begin{minipage}{0.8\linewidth}\centering\large\vspace{4pt}
`2(x + 3)` \;$\xrightarrow{\text{ expand }}$\; `2x + 6`
\qquad\qquad
`2x + 6` \;$\xrightarrow{\text{ factorise }}$\; `2(x + 3)`
\vspace{4pt}\end{minipage}}
\end{center}

\begin{stepsbox}{How to factorise}
\begin{enumerate}[nosep]
\item Find the \textbf{biggest number} (and/or \textbf{letter}) that goes into \textbf{every} term.
      Write it outside the bracket.
\item \textbf{Divide} each term by it. Write the answers inside the bracket.
\item \textbf{Check} by expanding --- you should get back to the question.
\end{enumerate}
\end{stepsbox}

\subsection*{Worked examples}
\begin{examples}
\example{5a + 10}{5 goes into both\\`5a ÷ 5 = a`,\; `10 ÷ 5 = 2`}{5(a + 2)}
\example{6x - 9}{3 goes into both\\`6x ÷ 3 = 2x`,\; `-9 ÷ 3 = -3`}{3(2x - 3)}
\example{x^2 + 4x}{`x` goes into both\\`x^2 ÷ x = x`,\; `4x ÷ x = 4`}{x(x + 4)}
\example{3x^2 + 6x}{`3x` goes into both\\`3x^2 ÷ 3x = x`,\; `6x ÷ 3x = 2`}{3x(x + 2)}
\example{14 - 7x}{7 goes into both\\`14 ÷ 7 = 2`,\; `-7x ÷ 7 = -x`}{7(2 - x)}
\example{8x - 12}{4 is the \textbf{biggest}\\(2 works, but isn't the biggest)}{4(2x - 3)}
\end{examples}

\begin{rememberbox}
Keep the sign with each term: in `6x - 9` the second term is `-9`, so the bracket has a minus: `3(2x - 3)`.
Always \textbf{check by expanding} your answer.
\end{rememberbox}
""",
    "practice": [
        ("3x + 6", "3(x + 2)"),
        ("2a + 8", "2(a + 4)"),
        ("4y - 12", "4(y - 3)"),
        ("6a + 9", "3(2a + 3)"),
        ("x^2 + 3x", "x(x + 3)"),
        ("x^2 - 2x", "x(x - 2)"),
        ("8x - 12", "4(2x - 3)"),
        ("6a - 15", "3(2a - 5)"),
        ("14 - 7x", "7(2 - x)"),
        ("ab + 3a", "a(b + 3)"),
        ("3x^2 + 6x", "3x(x + 2)"),
        ("2a^2 - 8a", "2a(a - 4)"),
    ],
    "check": [
        "5x + 20",
        "6a - 9",
        "x^2 + 8x",
        "4y^2 - 12y",
    ],
}

SECTIONS = [LIKE_TERMS, MULTIPLY, DIVIDE, EXPAND, FACTORISE]


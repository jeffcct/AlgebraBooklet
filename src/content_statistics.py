r"""Statistics workbook (easy level).

Same conventions as the algebra booklets (see content.py). The statistics
question types are described in stats.py. Every answer written here is checked
by the build against a calculation from the data: averages and quartiles,
correlation strength, the line of best fit (for predictions) and the plotted
points (for "describe a point in context").

Quartiles follow the class's dash method: draw dashes over the ordered numbers
until you reach the median, then cross dashes out in each half until you reach
the LQ and UQ (the median itself is left out of the halves).

Skill Check items carry no answers. A Skill Check strength plot needs to know
what to draw, so it has a "shows" setting instead; that is never printed.
"""
import stats as S

TITLE = "Statistics"
SUBTITLE = "Collect it. Show it. Make sense of it."
KICKER = "STATISTICS WORKBOOK"

CHOICE_PS = ["Primary", "Secondary"]
CHOICE_TYPE = ["Categorical", "Discrete numerical", "Continuous numerical"]
DISPLAY_OPTS = list(S.DISPLAYS.values())

# ---------------------------------------------------------------------------
# Scatter plots used in the booklet
# ---------------------------------------------------------------------------
ARMSPAN = {
    "title": "Height and arm span of 13 people",
    "points": [(152, 150), (156, 154), (158, 160), (162, 160), (164, 166), (168, 166), (170, 172),
               (174, 174), (176, 178), (180, 180), (184, 150), (186, 188), (188, 186)],
    "x": [150, 190, 2, 10], "y": [140, 190, 2, 10],
    "xlabel": "Height (cm)", "ylabel": "Arm span (cm)",
    "labels": {"A": (184, 150), "B": (170, 172)},
    "describe": "a person who is {x}\\,cm tall and has an arm span of {y}\\,cm",
}
ARMSPAN_FIT = dict(ARMSPAN, title="Height and arm span of 12 people",
                   points=[p for p in ARMSPAN["points"] if p != (184, 150)], labels={})

STUDY = {
    "title": "Hours of study and test score for 13 students",
    "points": [(1, 30), (2, 40), (3, 45), (3, 55), (4, 50), (5, 65), (6, 60), (6, 70), (7, 75),
               (8, 70), (9, 85), (10, 90), (9, 40)],
    "x": [0, 10, 1, 1], "y": [0, 100, 5, 10],
    "xlabel": "Hours of study", "ylabel": "Test score",
    "labels": {"A": (2, 40), "B": (5, 65), "C": (8, 70), "D": (10, 90), "E": (9, 40)},
    "describe": "a student who studied for {x} hours and scored {y} marks",
    "w": 6.4, "h": 5.4,
}

CHILDREN = {
    "title": "Age and height of 12 children",
    "points": [(5, 110), (6, 115), (7, 120), (7, 126), (8, 130), (9, 132), (10, 140), (11, 142),
               (12, 150), (13, 155), (9, 150), (14, 158)],
    "x": [4, 14, 1, 2], "y": [100, 170, 5, 10],
    "xlabel": "Age (years)", "ylabel": "Height (cm)",
    "labels": {"A": (6, 115), "B": (12, 150)},
    "describe": "a child who is {x} years old and {y}\\,cm tall",
    "w_check": 6.2, "h_check": 4.3,
}

CARS = {
    "title": "Age and value of 14 cars",
    "points": [(1, 27), (1, 25), (2, 24), (3, 21), (3, 23), (4, 19), (5, 17), (6, 16), (6, 13),
               (7, 12), (8, 10), (9, 8), (10, 5), (8, 7)],
    "x": [0, 10, 1, 1], "y": [0, 30, 1, 5],
    "xlabel": "Age (years)", "ylabel": r"Value (\$1000s)",
    "labels": {},
    "w": 6.4, "h": 6.0,
}

ICECREAM = {
    "title": "Temperature and ice creams sold on 13 days",
    "points": [(12, 20), (14, 30), (15, 25), (17, 40), (18, 50), (20, 55), (21, 50), (23, 70),
               (24, 80), (25, 75), (27, 95), (28, 90), (29, 105)],
    "x": [10, 30, 1, 5], "y": [0, 120, 5, 20],
    "xlabel": r"Temperature ($^\circ$C)", "ylabel": "Ice creams sold",
    "labels": {},
    "w": 6.4, "h": 6.0,
}

TRAVEL = {
    "title": "Distance from school and travel time for 12 students",
    "points": [(1, 5), (2, 8), (2, 10), (3, 12), (4, 14), (5, 18), (6, 20), (6, 24), (7, 25),
               (8, 28), (9, 32), (10, 34)],
    "x": [0, 10, 1, 1], "y": [0, 40, 2, 10],
    "xlabel": "Distance (km)", "ylabel": "Travel time (min)",
    "labels": {},
    "w_check": 6.2, "h_check": 4.3,
}

# ---------------------------------------------------------------------------
# 1. Data sources and types of data
# ---------------------------------------------------------------------------
DATA = {
    "id": "data",
    "num": 1,
    "title": "Data Sources and Types",
    "can": "I can tell primary from secondary data, and categorical from numerical data",
    "instr": "Circle the correct answer.",
    "check_instr": "Circle the correct answer.",
    "learn": r"""
\subsection*{Where does the data come from?}
\begin{center}
\renewcommand{\arraystretch}{1.25}
\begin{tabular}{|p{3.4cm}|p{6.1cm}|p{6.2cm}|}
\hline
\rowcolor{accentlight} & \textbf{What it means} & \textbf{Examples} \\ \hline
\textbf{Primary data} & You collect it \textbf{yourself}. & A survey you give your class; measuring heights; counting cars. \\ \hline
\textbf{Secondary data} & \textbf{Someone else} collected it. & A website, a newspaper, Stats NZ, a book, last year's survey. \\ \hline
\end{tabular}
\end{center}

\subsection*{What type of data is it?}
\begin{center}
\renewcommand{\arraystretch}{1.25}
\begin{tabular}{|p{3.4cm}|p{6.1cm}|p{6.2cm}|}
\hline
\rowcolor{accentlight}\textbf{Type} & \textbf{What it means} & \textbf{Examples} \\ \hline
\textbf{Categorical} & Words or groups, not numbers. & Favourite food, eye colour, type of pet. \\ \hline
\textbf{Discrete numerical} & Numbers you \textbf{count}. Usually whole numbers. & Number of pets, goals scored, people in a family. \\ \hline
\textbf{Continuous numerical} & Numbers you \textbf{measure}. Can have decimals. & Height, weight, time, temperature. \\ \hline
\end{tabular}
\end{center}

\begin{tipbox}{Ask yourself two questions}
1. Is the answer a \textbf{word} or a \textbf{number}? A word means \textbf{categorical}.\\
2. If it is a number, did you \textbf{count} it (\textbf{discrete}) or \textbf{measure} it (\textbf{continuous})?
\end{tipbox}

\subsection*{Worked examples}
\begin{examples}
\example{\text{Favourite sport}}{The answers are words like \textquotedblleft{}rugby\textquotedblright{}}{\textbf{Categorical}}
\example{\text{Number of siblings}}{You count them: 0, 1, 2, 3\ldots}{\textbf{Discrete}}
\example{\text{Time to run 100\,m}}{You measure it: 14.6 seconds}{\textbf{Continuous}}
\end{examples}
""",
    "practice": [
        {"type": "choice", "q": "Mere counts the cars that drive past the school gate in 10 minutes.", "options": CHOICE_PS, "a": "Primary"},
        {"type": "choice", "q": "Josh finds the populations of NZ cities on the Stats NZ website.", "options": CHOICE_PS, "a": "Secondary"},
        {"type": "choice", "q": "Ana measures the heights of everyone in her class.", "options": CHOICE_PS, "a": "Primary"},
        {"type": "choice", "q": "Tom uses rainfall data from a weather website.", "options": CHOICE_PS, "a": "Secondary"},
        {"type": "choice", "q": "Our class uses survey results that another class collected last year.", "options": CHOICE_PS, "a": "Secondary"},
        {"type": "choice", "q": "Type of data: \\textbf{favourite sport}", "options": CHOICE_TYPE, "a": "Categorical"},
        {"type": "choice", "q": "Type of data: \\textbf{number of pets}", "options": CHOICE_TYPE, "a": "Discrete numerical"},
        {"type": "choice", "q": "Type of data: \\textbf{time to run 100\\,m}", "options": CHOICE_TYPE, "a": "Continuous numerical"},
        {"type": "choice", "q": "Type of data: \\textbf{eye colour}", "options": CHOICE_TYPE, "a": "Categorical"},
        {"type": "choice", "q": "Type of data: \\textbf{goals scored in a game}", "options": CHOICE_TYPE, "a": "Discrete numerical"},
        {"type": "choice", "q": "Type of data: \\textbf{weight of a newborn baby}", "options": CHOICE_TYPE, "a": "Continuous numerical"},
        {"type": "choice", "q": "Type of data: \\textbf{texts sent in a day}", "options": CHOICE_TYPE, "a": "Discrete numerical"},
    ],
    "check": [
        {"type": "choice", "q": "Rawiri reads house prices in a newspaper.", "options": CHOICE_PS},
        {"type": "choice", "q": "Type of data: \\textbf{number of siblings}", "options": CHOICE_TYPE},
        {"type": "choice", "q": "Type of data: \\textbf{favourite colour}", "options": CHOICE_TYPE},
        {"type": "choice", "q": "Type of data: \\textbf{homework time}", "options": CHOICE_TYPE},
    ],
    "check_h": "4.9cm",
}

# ---------------------------------------------------------------------------
# 2. Data displays
# ---------------------------------------------------------------------------
def _display_row(kind, name, use):
    return (r"\raisebox{-0.5\height}{" + S.graph_picture(kind, w=3.2, h=2.0) + r"} & \textbf{" + name + "} & " + use + r" \\ \hline")


DISPLAYS = {
    "id": "displays",
    "num": 2,
    "title": "Data Displays",
    "can": "I can name a data display and choose the best one for some data",
    "instr": "Use these words: pie chart, bar graph, histogram, pictograph, line graph.",
    "check_instr": "Use: pie chart, bar graph, histogram, pictograph, line graph.",
    "practice_cols": 6,
    "learn": r"""
Different displays suit different kinds of data. Learn what each one looks like and what it is \textbf{for}.

\begin{center}
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{|>{\centering\arraybackslash}m{3.7cm}|m{2.6cm}|m{9cm}|}
\hline
\rowcolor{accentlight}\textbf{Looks like} & \textbf{Display} & \textbf{Use it for} \\ \hline
""" + _display_row("pie", "Pie chart", r"\textbf{Categorical} data, to show \textbf{parts of a whole} (fractions or percentages of the total).") + "\n"
    + _display_row("bar", "Bar graph", r"\textbf{Categorical} (or discrete) data, to \textbf{compare amounts}. The bars have \textbf{gaps} between them.") + "\n"
    + _display_row("histogram", "Histogram", r"\textbf{Continuous numerical} data in \textbf{groups} (like 150--155\,cm). The bars \textbf{touch} --- no gaps.") + "\n"
    + _display_row("pictograph", "Pictograph", r"\textbf{Categorical} data shown with \textbf{pictures}. There is always a \textbf{key} saying what one picture is worth.") + "\n"
    + _display_row("line", "Line graph", r"Showing how something \textbf{changes over time} (hours, days, months, years). The points are joined.") + "\n"
    + r"""\end{tabular}
\end{center}

\begin{rememberbox}
\textbf{Bar graph or histogram?} Look at the gaps. Bar graphs have gaps between the bars because each bar is a separate category.
Histograms have \textbf{no gaps} because the groups of numbers follow on from each other.
\end{rememberbox}

\begin{tipbox}{Choosing a display}
Is it about \textbf{time}? Use a line graph. \; Is it \textbf{parts of a whole}? Use a pie chart. \;
Is it \textbf{measured} data in groups? Use a histogram. \; Comparing \textbf{categories}? Use a bar graph or pictograph.
\end{tipbox}
""",
    "practice": [
        {"type": "identify", "graph": "bar", "a": "Bar graph", "span": 2},
        {"type": "identify", "graph": "pie", "a": "Pie chart", "span": 2},
        {"type": "identify", "graph": "line", "a": "Line graph", "span": 2},
        {"type": "identify", "graph": "histogram", "a": "Histogram", "span": 2},
        {"type": "identify", "graph": "pictograph", "a": "Pictograph", "span": 2},
        {"type": "identify", "graph": "histogram", "variant": 1, "a": "Histogram", "span": 2},
        {"type": "choice", "q": "Best display to show how the temperature changed each hour during a day?", "options": DISPLAY_OPTS, "a": "Line graph", "span": 3, "h": "2.9cm"},
        {"type": "choice", "q": "Best display to show what fraction of the class chose each favourite fruit?", "options": DISPLAY_OPTS, "a": "Pie chart", "span": 3, "h": "2.9cm"},
        {"type": "choice", "q": "Best display to compare how many students play rugby, netball, football and hockey?", "options": DISPLAY_OPTS, "a": "Bar graph", "span": 3, "h": "2.9cm"},
        {"type": "choice", "q": "Best display for the heights of 30 students, grouped into 150--155\\,cm, 155--160\\,cm, \\ldots?", "options": DISPLAY_OPTS, "a": "Histogram", "span": 3, "h": "2.9cm"},
        {"type": "choice", "q": "Best display to show books read by four friends, using a picture of a book for every 2 books?", "options": DISPLAY_OPTS, "a": "Pictograph", "span": 3, "h": "2.9cm"},
        {"type": "choice", "q": "Best display to show a shop's sales each month for a year?", "options": DISPLAY_OPTS, "a": "Line graph", "span": 3, "h": "2.9cm"},
    ],
    "check": [
        {"type": "identify", "graph": "line", "variant": 1},
        {"type": "identify", "graph": "histogram", "variant": 1},
        {"type": "choice", "q": "Best display to show how a baby's weight changed each month for a year?", "options": DISPLAY_OPTS},
        {"type": "choice", "q": "Best display to show the share of a budget spent on rent, food and power?", "options": DISPLAY_OPTS},
    ],
    "check_h": "4.6cm",
}

# ---------------------------------------------------------------------------
# 3. Scatter plots: points and strength
# ---------------------------------------------------------------------------
_mini = lambda target, seed: S.mini_scatter(S.strength_points(target, seed), w=3.0, h=2.2)

SCATTER = {
    "id": "scatter",
    "num": 3,
    "title": "Scatter Plots",
    "can": "I can describe a point in context, and the strength of a scatter plot",
    "instr": "Answer (a)--(e) using the scatter plot. Then describe each small scatter plot.",
    "check_instr": "Use the scatter plot.",
    "practice_cols": 6,
    "learn": r"""
A \textbf{scatter plot} shows \textbf{two numerical variables} for each person or thing. \textbf{Each dot is one person.}

\begin{minipage}[t]{0.5\linewidth}\vspace{0pt}\hspace*{8mm}""" + S.scatter_plot(ARMSPAN, 6.6, 5.0) + r"""\end{minipage}\hfill
\begin{minipage}[t]{0.46\linewidth}\vspace{0pt}
\textbf{Describing a point in context}\\[2pt]
Read \textbf{down} to the bottom axis and \textbf{across} to the side axis. Then write a sentence that uses
\textbf{both} variables and their \textbf{units}.\\[6pt]
\textbf{Point A} is """ + S.describe(ARMSPAN, "A") + r""".\\[6pt]
\textbf{Point B} is """ + S.describe(ARMSPAN, "B") + r""".\\[6pt]
Point A is \textbf{unusual}: it doesn't follow the pattern of the other points.
\end{minipage}

\vspace{9mm}
\subsection*{Describing the relationship}
\textbf{Direction:} \textbf{positive} if the points go \textbf{uphill} (as one goes up, the other goes up);
\textbf{negative} if they go \textbf{downhill}.\\
\textbf{Strength:} how closely the points follow a straight line.

\begin{center}
\begin{tabular}{cccc}
""" + _mini("strong positive", 1) + " & " + _mini("weak positive", 1) + " & " + _mini("strong negative", 1) + " & " + _mini("no relationship", 1) + r""" \\
\textbf{Strong positive} & \textbf{Weak positive} & \textbf{Strong negative} & \textbf{No relationship} \\
{\small Close to a line} & {\small Spread out, slight trend} & {\small Close to a line} & {\small No pattern}
\end{tabular}
\end{center}

\begin{rememberbox}
\textbf{Strong}: the points are close to a straight line. \textbf{Moderate}: they follow a line but are more spread out.
\textbf{Weak}: there is only a slight trend. Always give the \textbf{strength} and the \textbf{direction}, e.g. \textquotedblleft{}moderate positive\textquotedblright{}.
\end{rememberbox}
""",
    "practice": [
        {"type": "plotset", "plot": STUDY, "span": 6, "h": "10.8cm", "parts": [
            {"q": "describe", "point": "A"},
            {"q": "describe", "point": "B"},
            {"q": "describe", "point": "E"},
            {"q": "which", "at": (10, 90), "a": "D"},
            {"q": "strength", "a": "moderate positive"},
        ]},
        {"type": "strength", "seed": 3, "a": "strong positive", "span": 2},
        {"type": "strength", "seed": 3, "a": "moderate negative", "span": 2},
        {"type": "strength", "seed": 3, "a": "no relationship", "span": 2},
        {"type": "strength", "seed": 5, "a": "weak positive", "span": 2},
        {"type": "strength", "seed": 5, "a": "strong negative", "span": 2},
        {"type": "strength", "seed": 5, "a": "moderate positive", "span": 2},
    ],
    "check": [
        {"type": "plotset", "plot": CHILDREN, "parts": [
            {"q": "describe", "point": "A"},
            {"q": "describe", "point": "B"},
            {"q": "strength"},
        ]},
    ],
    "check_h": "7.5cm",
}

# ---------------------------------------------------------------------------
# 4. Lines of best fit and predictions
# ---------------------------------------------------------------------------
FIT = {
    "id": "fit",
    "num": 4,
    "title": "Lines of Best Fit",
    "can": "I can draw a line of best fit and use it to make a prediction",
    "instr": "Use a ruler to draw a line of best fit. Then use your line to make the predictions.",
    "check_instr": "Use a ruler.",
    "learn": r"""
A \textbf{line of best fit} is a straight line that shows the \textbf{trend} of the points.

\begin{stepsbox}{Drawing a line of best fit}
\begin{enumerate}[nosep]
\item Use a \textbf{ruler}. It must be a \textbf{straight} line.
\item Follow the \textbf{direction} of the points, through the \textbf{middle} of them.
\item Have about the \textbf{same number of points above and below} the line.
\item It does \textbf{not} have to go through (0,\,0), or through any particular point.
\end{enumerate}
\end{stepsbox}

\begin{minipage}[t]{0.5\linewidth}\vspace{0pt}\hspace*{8mm}""" + S.scatter_plot(ARMSPAN_FIT, 6.6, 5.2, line=True, preds=[166]) + r"""\end{minipage}\hfill
\begin{minipage}[t]{0.46\linewidth}\vspace{0pt}
\textbf{Making a prediction}\\[2pt]
Predict the arm span of a person who is \textbf{166\,cm} tall:
\begin{enumerate}[nosep]
\item Find 166 on the \textbf{bottom} axis.
\item Go \textbf{up} to your line.
\item Go \textbf{across} to the side axis and read the value.
\end{enumerate}
\vspace{3pt}
\textbf{Answer:} about \textbf{166\,cm}.\\[6pt]
To go the other way (from the side axis), go \textbf{across} to the line, then \textbf{down}.
\end{minipage}

\vspace{10mm}
\begin{rememberbox}
A prediction is an \textbf{estimate}, so say \textquotedblleft{}\textbf{about} 166\,cm\textquotedblright{}. Everyone's line is a little different,
so answers close to each other are all fine. Predictions are most reliable \textbf{inside} the range of the data.
\end{rememberbox}
""",
    "practice": [
        {"type": "plotset", "plot": CARS, "h": "9.6cm", "parts": [
            {"q": "draw"},
            {"q": "predict", "x": 2, "text": "Predict the value of a car that is 2 years old.",
             "a": 24, "tol": 2, "a_tpl": r"About \${v}\,000 (accept \${lo}\,000 to \${hi}\,000)."},
            {"q": "predict", "x": 7, "text": "Predict the value of a car that is 7 years old.",
             "a": 12, "tol": 2, "a_tpl": r"About \${v}\,000 (accept \${lo}\,000 to \${hi}\,000)."},
            {"q": "predict_x", "y": 15, "text": r"Predict the age of a car that is worth \$15\,000.",
             "a": 5.5, "tol": 1, "a_tpl": "About {v} years (accept {lo} to {hi} years)."},
        ]},
        {"type": "plotset", "plot": ICECREAM, "h": "9.6cm", "parts": [
            {"q": "draw"},
            {"q": "predict", "x": 16, "text": r"Predict the ice creams sold on a 16$^\circ$C day.",
             "a": 36, "tol": 8, "a_tpl": "About {v} (accept {lo} to {hi})."},
            {"q": "predict", "x": 26, "text": r"Predict the ice creams sold on a 26$^\circ$C day.",
             "a": 85, "tol": 8, "a_tpl": "About {v} (accept {lo} to {hi})."},
            {"q": "predict_x", "y": 60, "text": "Predict the temperature on a day when 60 ice creams were sold.",
             "a": 21, "tol": 2, "a_tpl": r"About {v}$^\circ$C (accept {lo} to {hi}$^\circ$C)."},
        ]},
    ],
    "check": [
        {"type": "plotset", "plot": TRAVEL, "parts": [
            {"q": "draw"},
            {"q": "predict", "x": 5, "text": "Predict the travel time for a student who lives 5\\,km from school."},
            {"q": "predict_x", "y": 30, "text": "Predict how far away a student lives if their trip takes 30 minutes."},
        ]},
    ],
    "check_h": "6.9cm",
}

# ---------------------------------------------------------------------------
# 5. Centres: mean, median, mode
# ---------------------------------------------------------------------------
CENTRES = {
    "id": "centres",
    "num": 5,
    "title": "Mean, Median and Mode",
    "can": "I can find the mean, median and mode of a set of data",
    "instr": "Order the numbers first, then find the answer.",
    "check_instr": "Show your working.",
    "learn": r"""
\begin{center}
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|p{2.2cm}|p{13.2cm}|}
\hline
\textbf{Mode} & The value that appears \textbf{most often}. \\ \hline
\textbf{Median} & The \textbf{middle} value when the numbers are \textbf{in order}. \\ \hline
\textbf{Mean} & \textbf{Add} all the numbers, then \textbf{divide} by how many there are. \\ \hline
\end{tabular}
\end{center}

\subsection*{Example: 7, 3, 9, 4, 7}
\textbf{Step 1: put the numbers in order.} \quad 3, 4, 7, 7, 9

\textbf{Mode:} 7 appears twice, more than any other number. \quad Mode $= 7$

\textbf{Median:} draw a dash over the numbers from \textbf{each end}, one at a time, until you reach the middle.\par
\hspace*{10mm}""" + S.dashes([3, 4, 7, 7, 9], "median") + r"""\hspace{8mm} Median $= 7$

\textbf{Mean:} $3 + 4 + 7 + 7 + 9 = 30$, \quad and there are 5 numbers, \quad so $30 \div 5 = 6$. \quad Mean $= 6$

\subsection*{When there is an even number of values}
The dashes meet \textbf{between two numbers}. The median is \textbf{halfway} between them.\par
\hspace*{10mm}""" + S.dashes([2, 5, 6, 8, 10, 12], "median") + r"""\hspace{8mm} Median $= \dfrac{6 + 8}{2} = 7$

\begin{rememberbox}
\textbf{Always order the numbers first} for the median. The mean and median can be decimals, e.g. 7.5.
\end{rememberbox}
""",
    "practice": [
        {"type": "stat", "ask": "mode", "data": [3, 5, 5, 6, 8], "a": 5},
        {"type": "stat", "ask": "mode", "data": [4, 9, 7, 2, 7, 4, 7], "a": 7},
        {"type": "stat", "ask": "median", "data": [2, 4, 7, 9, 10], "a": 7},
        {"type": "stat", "ask": "median", "data": [11, 3, 8, 5, 6], "a": 6},
        {"type": "stat", "ask": "median", "data": [21, 18, 25, 18, 30, 22, 19], "a": 21},
        {"type": "stat", "ask": "median", "data": [4, 6, 9, 12], "a": 7.5},
        {"type": "stat", "ask": "median", "data": [15, 10, 20, 25, 30, 5], "a": 17.5},
        {"type": "stat", "ask": "mean", "data": [2, 4, 6, 8], "a": 5},
        {"type": "stat", "ask": "mean", "data": [5, 7, 9, 3, 6], "a": 6},
        {"type": "stat", "ask": "mean", "data": [10, 12, 14, 16, 18], "a": 14},
        {"type": "stat", "ask": "mean", "data": [3, 8, 6, 7], "a": 6},
        {"type": "stat", "ask": "mean", "data": [12, 15, 9, 20, 14, 8], "a": 13},
    ],
    "check": [
        {"type": "stat", "ask": "mode", "data": [6, 3, 8, 3, 9, 3]},
        {"type": "stat", "ask": "median", "data": [9, 4, 12, 7, 15]},
        {"type": "stat", "ask": "median", "data": [3, 8, 10, 13]},
        {"type": "stat", "ask": "mean", "data": [4, 9, 5, 10, 7]},
    ],
    "check_h": "3.7cm",
}

# ---------------------------------------------------------------------------
# 6. Spread: range, quartiles, IQR
# ---------------------------------------------------------------------------
SPREAD = {
    "id": "spread",
    "num": 6,
    "title": "Range and Quartiles",
    "can": "I can find the range, LQ, UQ and IQR of a set of data",
    "instr": "Order the numbers first. Use the dash method for the median and quartiles.",
    "check_instr": "Order the numbers first.",
    "practice_cols": 6,
    "learn": r"""
The \textbf{spread} tells you how spread out the data is.

\begin{center}
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|p{4.2cm}|p{11.2cm}|}
\hline
\textbf{Range} & Biggest value $-$ smallest value. \\ \hline
\textbf{Lower quartile (LQ)} & The middle of the \textbf{lower half} of the data. \\ \hline
\textbf{Upper quartile (UQ)} & The middle of the \textbf{upper half} of the data. \\ \hline
\textbf{Interquartile range (IQR)} & $\text{UQ} - \text{LQ}$. The spread of the middle half of the data. \\ \hline
\end{tabular}
\end{center}

\subsection*{Example: 9, 2, 14, 5, 11, 3, 18, 8, 15, 6, 12}
\textbf{Step 1: put the numbers in order.} \quad 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 18

\textbf{Range:} $18 - 2 = 16$

\textbf{Step 2: find the median.} Draw dashes over the numbers from each end until you reach the middle.\par
\hspace*{6mm}""" + S.dashes([2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 18], "median") + r"""

\textbf{Step 3: find the quartiles.} The median splits the data into two halves (the median is \textbf{not} in either half).
In each half, cross out the dashes from each end until you reach the middle of that half.\par
\hspace*{6mm}""" + S.dashes([2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 18], "quartiles") + r"""

\textbf{LQ} $= 5$, \quad \textbf{UQ} $= 14$, \quad \textbf{IQR} $= 14 - 5 = 9$

\begin{rememberbox}
If a half has an \textbf{even} number of values, the quartile is \textbf{halfway} between the two middle numbers ---
the same as for the median.
\end{rememberbox}
""",
    "practice": [
        {"type": "stat", "ask": "range", "data": [4, 9, 2, 12, 7], "a": 10, "span": 2, "h": "3.0cm"},
        {"type": "stat", "ask": "range", "data": [15, 22, 18, 30, 11], "a": 19, "span": 2, "h": "3.0cm"},
        {"type": "stat", "ask": "range", "data": [35, 42, 28, 50, 47, 31], "a": 22, "span": 2, "h": "3.0cm"},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [2, 4, 5, 7, 9, 10, 12],
         "a": {"median": 7, "lq": 4, "uq": 10, "iqr": 6}, "span": 3},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [12, 5, 9, 20, 15, 7, 18],
         "a": {"median": 12, "lq": 7, "uq": 18, "iqr": 11}, "span": 3},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [3, 6, 8, 9, 11, 14, 15, 18, 20, 22, 25],
         "a": {"median": 14, "lq": 8, "uq": 20, "iqr": 12}, "span": 3},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [45, 32, 50, 38, 41, 29, 36, 47, 40, 33, 52],
         "a": {"median": 40, "lq": 33, "uq": 47, "iqr": 14}, "span": 3},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [10, 12, 15, 16, 18, 21, 22, 25, 30],
         "a": {"median": 18, "lq": 13.5, "uq": 23.5, "iqr": 10}, "span": 3},
        {"type": "spread", "ask": ["median", "lq", "uq", "iqr"], "data": [1, 3, 4, 6, 7, 9, 10, 12],
         "a": {"median": 6.5, "lq": 3.5, "uq": 9.5, "iqr": 6}, "span": 3},
    ],
    "check": [
        {"type": "stat", "ask": "range", "data": [8, 3, 14, 6, 11]},
        {"type": "spread", "ask": ["lq", "uq", "iqr"], "data": [13, 4, 9, 6, 15, 7, 12]},
    ],
    "check_h": "4.6cm",
}

SECTIONS = [DATA, DISPLAYS, SCATTER, FIT, CENTRES, SPREAD]

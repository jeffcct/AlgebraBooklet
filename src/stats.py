r"""Statistics question types for build.py: drawing (TikZ), answer checking and answers.

Question types (dicts with a "type"):
  choice    {"q": text, "options": [...], "a": option}        circle one (<= 3 options) or write from the word bank
  identify  {"graph": "pie"|"bar"|"histogram"|"pictograph"|"line", "a": name}   name the display shown
  strength  {"seed": n, "a": "strong positive"|... }           a small scatter plot; describe its strength
  stat      {"data": [...], "ask": "mean"|"median"|"mode"|"range", "a": value}
  spread    {"data": [...], "ask": [...of median/lq/uq/iqr/range], "a": {...}}
  plotset   {"plot": {...}, "parts": [...]}                     a scatter plot with several part-questions

Every answer written in the content file is checked here against a calculation
from the data: the averages and quartiles, the correlation (for strength), the
regression line (for predictions) and the plotted points (for "describe a point").

Quartiles use the class's dash method, which is the "median of each half"
method: find the median, split the ordered data at it (leaving the median out
when it is one of the numbers), then find the middle of each half.
"""
import math
import random

TYPES = {"choice", "identify", "strength", "stat", "spread", "plotset"}

DISPLAYS = {"pie": "Pie chart", "bar": "Bar graph", "histogram": "Histogram",
            "pictograph": "Pictograph", "line": "Line graph"}

# ---------------------------------------------------------------------------
# Number helpers
# ---------------------------------------------------------------------------

def fmt(v):
    """7.0 -> '7', 7.5 -> '7.5', 7.25 -> '7.25'"""
    v = round(float(v), 2)
    return str(int(v)) if v == int(v) else f"{v:g}"


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def halves(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[:n // 2], xs[(n + 1) // 2:]


def summary(xs):
    lo, hi = halves(xs)
    lq, uq = median(lo), median(hi)
    counts = {v: xs.count(v) for v in xs}
    top = max(counts.values())
    modes = [v for v, c in counts.items() if c == top]
    return {"mean": sum(xs) / len(xs), "median": median(xs), "lq": lq, "uq": uq,
            "iqr": uq - lq, "range": max(xs) - min(xs),
            "mode": modes[0] if len(modes) == 1 and top > 1 else None}


def correlation(pts):
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxy = sum((x - mx) * (y - my) for x, y in pts)
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    syy = sum((y - my) ** 2 for _, y in pts)
    return sxy / math.sqrt(sxx * syy)


def regression(pts):
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    m = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return m, my - m * mx


def strength_of(r):
    a = abs(r)
    word = "strong" if a >= 0.8 else "moderate" if a >= 0.5 else "weak" if a >= 0.25 else None
    if word is None:
        return "no relationship"
    return f"{word} {'positive' if r > 0 else 'negative'}"


STRENGTH_TARGET = {  # strength -> (slope sign, noise)
    "strong positive": (1, 0.6), "moderate positive": (1, 1.9), "weak positive": (1, 3.2),
    "strong negative": (-1, 0.6), "moderate negative": (-1, 1.9), "weak negative": (-1, 3.2),
    "no relationship": (0, 0)}
BANDS = {"strong": (0.85, 1.0), "moderate": (0.58, 0.72), "weak": (0.3, 0.42), "no": (0.0, 0.1)}


def strength_points(target, seed):
    """Deterministic points for a small scatter plot that clearly shows `target`.
    Tries seeds from `seed` upwards until |r| sits well inside the target's band."""
    sign, noise = STRENGTH_TARGET[target]
    lo, hi = BANDS[target.split()[0]]
    for s in range(seed, seed + 500):
        rng = random.Random(s)
        xs = [rng.uniform(0.5, 9.5) for _ in range(16)]
        if sign == 0:
            pts = [(x, rng.uniform(1, 9)) for x in xs]
        else:
            pts = [(x, 5 + sign * 0.8 * (x - 5) + rng.gauss(0, noise)) for x in xs]
        if all(0.3 <= y <= 9.7 for _, y in pts) and lo <= abs(correlation(pts)) <= hi \
                and (sign == 0 or (correlation(pts) > 0) == (sign > 0)):
            return pts
    raise ValueError(f"could not make a '{target}' plot from seed {seed}")


# ---------------------------------------------------------------------------
# TikZ drawings
# ---------------------------------------------------------------------------

def mini_scatter(pts, w=3.6, h=2.7):
    out = [r"\begin{tikzpicture}[x=%.4fcm,y=%.4fcm]" % (w / 10, h / 10),
           r"\draw[thick,->,>=stealth] (0,0) -- (10.3,0); \draw[thick,->,>=stealth] (0,0) -- (0,10.3);"]
    out += [r"\fill (%.2f,%.2f) circle (1.5pt);" % p for p in pts]
    out.append(r"\end{tikzpicture}")
    return "".join(out)


def scatter_plot(plot, w=None, h=None, line=False, preds=()):
    """A gridded scatter plot. `plot` = {"points": [...], "x": [lo, hi, grid, label_every],
    "y": [...], "xlabel", "ylabel", "labels": {"A": [x, y]}}. Optional line of best fit and
    dashed prediction lines (x values)."""
    x0, x1, xg, xl = plot["x"]
    y0, y1, yg, yl = plot["y"]
    w = w or plot.get("w", 8.0)
    h = h or plot.get("h", 6.0)
    sx, sy = w / (x1 - x0), h / (y1 - y0)
    X, Y = x1 - x0, y1 - y0
    out = [r"\begin{tikzpicture}[x=%.5fcm,y=%.5fcm, baseline=(current bounding box.north)]" % (sx, sy)]
    k = x0
    while k <= x1 + 1e-9:
        out.append(r"\draw[black!14] (%g,0) -- (%g,%g);" % (k - x0, k - x0, Y))
        if abs(((k - x0) / xl) - round((k - x0) / xl)) < 1e-9:
            out.append(r"\node[below, font=\scriptsize] at (%g,0) {%s};" % (k - x0, fmt(k)))
        k += xg
    k = y0
    while k <= y1 + 1e-9:
        out.append(r"\draw[black!14] (0,%g) -- (%g,%g);" % (k - y0, X, k - y0))
        if abs(((k - y0) / yl) - round((k - y0) / yl)) < 1e-9:
            out.append(r"\node[left, font=\scriptsize] at (0,%g) {%s};" % (k - y0, fmt(k)))
        k += yg
    out.append(r"\draw[thick] (0,%g) -- (0,0) -- (%g,0);" % (Y, X))
    out.append(r"\node[below=11pt, font=\small] at (%g,0) {%s};" % (X / 2, plot["xlabel"]))
    out.append(r"\node[rotate=90, above=17pt, font=\small] at (0,%g) {%s};" % (Y / 2, plot["ylabel"]))
    if line:
        m, c = regression(plot["points"])
        xa, xb = x0, x1
        ya, yb = m * xa + c, m * xb + c
        # clip the line to the plotting area
        def clip(xv, yv, other_x):
            if yv > y1:
                return (y1 - c) / m, y1
            if yv < y0:
                return (y0 - c) / m, y0
            return xv, yv
        xa, ya = clip(xa, ya, xb)
        xb, yb = clip(xb, yb, xa)
        out.append(r"\draw[accent, very thick] (%g,%g) -- (%g,%g);" % (xa - x0, ya - y0, xb - x0, yb - y0))
        for px in preds:
            py = m * px + c
            out.append(r"\draw[checkcol, thick, dashed, ->, >=stealth] (%g,0) -- (%g,%g) -- (0,%g);"
                       % (px - x0, px - x0, py - y0, py - y0))
    for x, y in plot["points"]:
        out.append(r"\fill (%g,%g) circle (1.7pt);" % (x - x0, y - y0))
    for name, (x, y) in plot.get("labels", {}).items():
        out.append(r"\node[above right=-1pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] at (%g,%g) {%s};"
                   % (x - x0, y - y0, name))
    out.append(r"\end{tikzpicture}")
    return "".join(out)


def graph_picture(kind, variant=0, w=3.8, h=2.6):
    """Small example displays to identify."""
    o = [r"\begin{tikzpicture}[x=%.4fcm,y=%.4fcm]" % (w / 10, h / 10)]
    axes = r"\draw[thick] (0,10) -- (0,0) -- (10,0);"
    if kind == "pie":
        sets = [[0, 140, 230, 300, 360], [0, 180, 270, 360]][variant % 2]
        cols = ["accent", "accentlight", "warmedge", "checklight"]
        o = [r"\begin{tikzpicture}"]
        for i in range(len(sets) - 1):
            o.append(r"\filldraw[fill=%s, draw=white, thick] (0,0) -- (%d:1.15) arc (%d:%d:1.15) -- cycle;"
                     % (cols[i], sets[i], sets[i], sets[i + 1]))
        o.append(r"\draw[thick] (0,0) circle (1.15);")
    elif kind == "bar":
        o.append(axes)
        hs = [[7, 4, 9, 5], [3, 8, 6, 9]][variant % 2]
        for i, v in enumerate(hs):
            xa = 0.8 + i * 2.4
            o.append(r"\filldraw[fill=accent, draw=accent] (%g,0) rectangle (%g,%g);" % (xa, xa + 1.5, v))
            o.append(r"\node[below, font=\tiny] at (%g,0) {%s};" % (xa + 0.75, "ABCD"[i]))
    elif kind == "histogram":
        o.append(axes)
        hs = [[3, 6, 9, 7, 4], [2, 5, 8, 9, 5]][variant % 2]
        for i, v in enumerate(hs):
            o.append(r"\filldraw[fill=accentlight, draw=accent, thick] (%g,0) rectangle (%g,%g);" % (i * 2, i * 2 + 2, v))
        for i in range(6):
            o.append(r"\node[below, font=\tiny] at (%g,0) {%d};" % (i * 2, 10 + i * 10))
    elif kind == "pictograph":
        rows = [[4, 2, 5], [3, 5, 2]][variant % 2]
        o = [r"\begin{tikzpicture}[x=0.42cm,y=0.5cm]"]
        for r, n in enumerate(rows):
            o.append(r"\node[left, font=\tiny] at (0,%g) {%s};" % (-r, ["Mon", "Tue", "Wed"][r]))
            for i in range(n):
                o.append(r"\fill[accent] (%g,%g) circle (0.17);" % (0.5 + i * 0.8, -r))
        o.append(r"\node[font=\tiny, anchor=west] at (-1.4,-3) {Key: \tikz\fill[accent] (0,0) circle (0.07cm); = 2 people};")
    elif kind == "line":
        o.append(axes)
        ys = [[2, 4, 3.5, 6, 7.5, 7], [8, 6.5, 7, 5, 3, 2.5]][variant % 2]
        pts = [(0.8 + i * 1.75, v) for i, v in enumerate(ys)]
        o.append(r"\draw[accent, thick] " + " -- ".join("(%g,%g)" % p for p in pts) + ";")
        o += [r"\fill[accent] (%g,%g) circle (1.6pt);" % p for p in pts]
        for i, mth in enumerate("JFMAMJ"):
            o.append(r"\node[below, font=\tiny] at (%g,0) {%s};" % (0.8 + i * 1.75, mth))
    else:
        raise ValueError(kind)
    o.append(r"\end{tikzpicture}")
    return "".join(o)


def dashes(data, stage):
    """The class's dash method, drawn on ordered data.
    stage 'median': dashes over every number except the middle; the median is circled
    (or marked between the two middle numbers).
    stage 'quartiles': the dashes in each half are crossed out except the middle of each half,
    which is circled as the LQ and UQ."""
    xs = sorted(data)
    n = len(xs)
    gap = 1.0
    o = [r"\begin{tikzpicture}[baseline=-1mm]"]
    for i, v in enumerate(xs):
        o.append(r"\node[font=\large] (n%d) at (%g,0) {%s};" % (i, i * gap, fmt(v)))

    def mark(pos, label, colour):
        if pos == int(pos):
            o.append(r"\draw[%s, very thick] (%g,0) circle (0.36);" % (colour, pos * gap))
        else:
            o.append(r"\draw[%s, very thick] (%g,-0.35) -- (%g,0.35);" % (colour, pos * gap, pos * gap))
        o.append(r"\node[%s, font=\small\bfseries] at (%g,-0.7) {%s};" % (colour, pos * gap, label))

    mpos = (n - 1) / 2
    lower = list(range(0, n // 2))
    upper = list(range((n + 1) // 2, n))
    lq_pos = (lower[0] + lower[-1]) / 2
    uq_pos = (upper[0] + upper[-1]) / 2
    for i in range(n):
        if i == mpos:
            continue
        x = i * gap
        o.append(r"\draw[thick] (%g,0.5) -- (%g,0.5);" % (x - 0.18, x + 0.18))
        if stage == "quartiles" and i not in (lq_pos, uq_pos):
            o.append(r"\draw[checkcol, thick] (%g,0.36) -- (%g,0.64);" % (x - 0.12, x + 0.12))
    mark(mpos, "median", "accent")
    if stage == "quartiles":
        mark(lq_pos, "LQ", "checkcol")
        mark(uq_pos, "UQ", "checkcol")
    o.append(r"\end{tikzpicture}")
    return "".join(o)


# ---------------------------------------------------------------------------
# Checking
# ---------------------------------------------------------------------------

def _point(plot, name):
    return plot["labels"][name]


def describe(plot, name):
    x, y = _point(plot, name)
    return plot["describe"].format(x=fmt(x), y=fmt(y))


def part_answer(plot, p):
    """The answer to one part of a plotset, calculated from the plot (None for 'draw')."""
    q = p["q"]
    if q == "describe":
        return f"Point {p['point']} is {describe(plot, p['point'])}."
    if q == "which":
        hits = [k for k, v in plot["labels"].items() if list(v) == list(p["at"])]
        return hits[0] if len(hits) == 1 else None
    if q == "strength":
        return strength_of(correlation(plot["points"]))
    if q == "draw":
        return None
    m, c = regression(plot["points"])
    if q == "predict":
        return m * p["x"] + c
    if q == "predict_x":
        return (p["y"] - c) / m
    raise ValueError(q)


def check_part(plot, p):
    q = p["q"]
    if q == "describe":
        return [] if p["point"] in plot["labels"] else [f"there is no point {p['point']}"]
    if q == "which":
        hit = part_answer(plot, p)
        if hit is None:
            return [f"no single labelled point at {p['at']}"]
        if "a" in p and p["a"] != hit:
            return [f"answer {p['a']} but the point at {p['at']} is {hit}"]
        return []
    if q == "strength":
        real = part_answer(plot, p)
        return [] if "a" not in p or p["a"] == real else [f"strength is '{real}' (r = {correlation(plot['points']):.2f}), not '{p['a']}'"]
    if q in ("predict", "predict_x"):
        real = part_answer(plot, p)
        if "a" in p and abs(p["a"] - real) > p["tol"] / 2:
            return [f"prediction {p['a']} is too far from the line's value {real:.2f}"]
        return []
    if q == "draw":
        return []
    return [f"unknown part '{q}'"]


def check(it):
    t = it["type"]
    if t == "choice":
        return [] if it["a"] in it["options"] else [f"answer '{it['a']}' is not one of the options"]
    if t == "identify":
        return [] if it["a"] == DISPLAYS[it["graph"]] else [f"a {it['graph']} is a {DISPLAYS[it['graph']]}, not '{it['a']}'"]
    if t == "strength":
        pts = strength_points(it["a"], it["seed"])
        real = strength_of(correlation(pts))
        return [] if real == it["a"] else [f"plot shows '{real}', not '{it['a']}'"]
    if t == "stat":
        real = summary(it["data"])[it["ask"]]
        if real is None:
            return ["data has no single mode"]
        return [] if math.isclose(real, float(it["a"])) else [f"{it['ask']} is {fmt(real)}, not {it['a']}"]
    if t == "spread":
        s = summary(it["data"])
        return [f"{k} is {fmt(s[k])}, not {it['a'][k]}" for k in it["ask"] if not math.isclose(s[k], float(it["a"][k]))]
    if t == "plotset":
        errs = []
        for i, p in enumerate(it["parts"]):
            errs += [f"part ({'abcdefgh'[i]}): {e}" for e in check_part(it["plot"], p)]
        return errs
    return [f"unknown type {t}"]


def check_question(it):
    """Skill Check items: questions only, no answers stored."""
    if "a" in it or any("a" in p for p in it.get("parts", [])):
        return ["Skill Check questions must not include an answer"]
    t = it["type"]
    if t == "strength":
        strength_points(it["shows"], it["seed"])
    if t == "plotset":
        for p in it["parts"]:
            if p["q"] == "describe" and p["point"] not in it["plot"]["labels"]:
                return [f"there is no point {p['point']}"]
    return []


def marks(it):
    if it["type"] == "plotset":
        return len(it["parts"])
    if it["type"] == "spread":
        return len(it["ask"])
    return 1


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

ASK_NAME = {"mean": "Mean", "median": "Median", "mode": "Mode", "range": "Range",
            "lq": "LQ", "uq": "UQ", "iqr": "IQR"}


def data_tex(xs):
    """Plain text (not maths) so long lists can wrap onto a second line."""
    return ", ".join(fmt(v) for v in xs)


def part_text(plot, p):
    q = p["q"]
    if q == "describe":
        return f"Describe point \\textbf{{{p['point']}}} in context."
    if q == "which":
        x, y = p["at"]
        return "Which point is " + plot["describe"].format(x=fmt(x), y=fmt(y)) + "?"
    if q == "strength":
        return "Describe the strength and direction of the relationship."
    if q == "draw":
        return "Draw a line of best fit on the graph."
    return p["text"]


def body(it, compact):
    t = it["type"]
    txt = r"\normalsize" if compact else r"\large"
    if t == "choice":
        q = rf"{{{txt} {it['q']}}}\par\vfill "
        if len(it["options"]) <= 3:
            sep = r"\par\vspace{1mm}" if compact else r"\quad "
            opts = (r"{\footnotesize" if compact else r"{\small") + r"\raggedright " + sep.join(rf"\fbox{{\strut\ {o}\ }}" for o in it["options"]) + "}"
            return q + r"{\small Circle one:}\par\vspace{1mm}" + opts
        return q + r"\ansline{0.95}"
    if t == "identify":
        size = {"w": 3.3, "h": 2.4} if compact else {}
        return (r"\par\centering " + graph_picture(it["graph"], it.get("variant", 0), **size) +
                r"\par\vfill\raggedright This is a\ \ansline{0.6}")
    if t == "strength":
        pts = strength_points(it.get("a") or it["shows"], it["seed"])
        return r"\par\centering " + mini_scatter(pts) + r"\par\vfill\raggedright\ansline{0.95}"
    if t == "stat":
        name = ASK_NAME[it["ask"]]
        return (rf"\raggedright{{{txt} Find the \textbf{{{name.lower()}}}:}}\par\vspace{{1mm}}"
                rf"{{{txt} {data_tex(it['data'])}}}\par\vfill "
                rf"{name} $=$\ \ansline{{0.55}}")
    if t == "spread":
        lines = r"\par\vfill ".join(rf"{ASK_NAME[k]} $=$\ \ansline{{0.45}}" for k in it["ask"])
        return (rf"\raggedright{{{txt} {data_tex(it['data'])}}}\par\vspace{{2mm}}" + lines)
    if t == "plotset":
        plot = it["plot"]
        pw = plot.get("w_check" if compact else "w", 6.4)
        ph = plot.get("h_check" if compact else "h", 6.0)
        parts = []
        for i, p in enumerate(it["parts"]):
            line = "" if p["q"] == "draw" else r"\par\vspace{4mm}\ansline{1}"
            parts.append(rf"{{\small\textbf{{({'abcdefgh'[i]})}} {part_text(plot, p)}}}" + line)
        gapsize = "1.5mm" if compact else "3mm"
        return (rf"\textbf{{{plot['title']}}}\par\vspace{{1mm}}"
                r"\begin{minipage}[t]{0.52\linewidth}\vspace{0pt}\hspace*{9mm}" + scatter_plot(plot, pw, ph) +
                r"\end{minipage}\hfill\begin{minipage}[t]{0.46\linewidth}\vspace{0pt}" +
                (r"\par\vspace{%s}" % gapsize).join(parts) + r"\end{minipage}")
    raise ValueError(t)


def answer(it):
    t = it["type"]
    if t in ("choice", "identify", "strength"):
        return it["a"]
    if t == "stat":
        return fmt(it["a"])
    if t == "spread":
        return ", ".join(f"{ASK_NAME[k]} = {fmt(it['a'][k])}" for k in it["ask"])
    if t == "plotset":
        out = []
        for i, p in enumerate(it["parts"]):
            letter = "abcdefgh"[i]
            if p["q"] == "draw":
                a = "A straight line through the middle of the points, with about the same number of points above and below it."
            elif p["q"] in ("predict", "predict_x"):
                a = p["a_tpl"].format(v=fmt(p["a"]), lo=fmt(p["a"] - p["tol"]), hi=fmt(p["a"] + p["tol"]))
            elif p["q"] == "strength":
                a = p["a"][0].upper() + p["a"][1:] + "."
            else:
                a = part_answer(it["plot"], p)
            out.append(rf"\textbf{{({letter})}} {a}")
        return r"\quad ".join(out)
    raise ValueError(t)


# default sizes / layout for build.py
PRACTICE_H = {"choice": "3.1cm", "identify": "4.4cm", "strength": "4.3cm", "stat": "3.3cm",
              "spread": "5.6cm", "plotset": "8.3cm"}
PRACTICE_SPAN = {"plotset": 2}   # in a 2-column grid; sections with 6 columns set spans themselves
CHECK_SPAN = {"choice": 1, "identify": 1, "strength": 1, "stat": 1, "spread": 3, "plotset": 4}
ANSWER_COLS = {"plotset": 1, "spread": 1, "choice": 2, "identify": 3, "strength": 3, "stat": 4}

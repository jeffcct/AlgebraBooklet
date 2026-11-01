#!/usr/bin/env python3
"""Build the student booklet and teacher answer key.

    python3 src/build.py          # check answers, write HTML to build/
    node src/make_pdf.js          # turn build/*.html into PDFs in the repo root

The check step evaluates every question and its answer at lots of random
values and stops the build if any answer is wrong, isn't simplified, or
isn't fully factorised.
"""
import html
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")

# ---------------------------------------------------------------------------
# Answer checking
# ---------------------------------------------------------------------------

def to_python(expr):
    """'3x^2 + 2(x - 1)' -> '3*x**2 + 2*(x - 1)'. Single-letter variables."""
    s = expr.replace(" ", "").replace("×", "*").replace("−", "-")
    if "÷" in s:
        num, den = s.split("÷")
        s = f"({num})/({den})"
    s = s.replace("^", "**")
    out = []
    for i, ch in enumerate(s):
        if out:
            prev = out[-1][-1]
            # implicit multiplication: 3x, xy, 2(, x(, )(, )x
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
    """Split '3x^2 - 2x + 5' into ['3x^2', '-2x', '+5'] (no brackets expected)."""
    return re.findall(r"[+-]?\s*[^+-]+", expr.replace(" ", ""))


def letter_part(term):
    t = term.lstrip("+-")
    t = re.sub(r"^\d+", "", t)
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
    for t in terms(a):
        if re.match(r"^[+-]?1[a-z]", t):
            problems.append("answer writes a coefficient of 1")
    return problems


def check_factorised(q, a):
    problems = []
    if "(" not in a:
        problems.append("answer has no brackets")
    m = re.fullmatch(r"(\d*[a-z]?)\((.*)\)", a.replace(" ", ""))
    if m:  # common-factor form k(...)
        inside = terms(m.group(2))
        coeffs = [int(re.match(r"[+-]?(\d*)", t).group(1) or 1) for t in inside]
        if math.gcd(*coeffs) != 1:
            problems.append("number factor left inside the bracket")
        letter_sets = [set(re.findall(r"[a-z]", t)) for t in inside]
        if set.intersection(*letter_sets):
            problems.append("letter factor left inside the bracket")
    return problems


def check_all():
    errors = []
    count = 0

    def check(where, q, a, kind):
        nonlocal count
        count += 1
        if not same(q, a):
            errors.append(f"{where}: '{q}' is NOT equal to '{a}'")
        probs = check_factorised(q, a) if kind == "factorise" else check_simplified(a)
        for p in probs:
            errors.append(f"{where}: '{q}' -> '{a}': {p}")

    for s in C.SECTIONS:
        for part in ("practice_a", "practice_b", "check"):
            for i, (q, a) in enumerate(s[part], 1):
                check(f"S{s['num']} {part} Q{i}", q, a, s["kind"])
    for i, (sec, q, a) in enumerate(C.MIXED, 1):
        check(f"Mixed Q{i}", q, a, C.SECTIONS[sec - 1]["kind"])
    return count, errors


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def m(expr):
    """Typeset a plain-text expression."""
    out = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == "^":
            j = i + 1
            while j < len(expr) and expr[j].isdigit():
                j += 1
            out.append(f"<sup>{expr[i+1:j]}</sup>")
            i = j
            continue
        if ch.isalpha() and ch.isascii():
            out.append(f"<i>{ch}</i>")
        elif ch == "-":
            out.append("−")
        else:
            out.append(html.escape(ch))
        i += 1
    return f'<span class="m">{"".join(out)}</span>'


def rich(text):
    """Replace `maths` in HTML notes with typeset maths."""
    return re.sub(r"`([^`]+)`", lambda mo: m(mo.group(1)), text)


def esc(t):
    return html.escape(t)


def page(body, cls=""):
    return f'<section class="page {cls}">{body}</section>'


def section_banner(s, label):
    return (f'<div class="banner"><span class="bn">{s["num"]}</span>'
            f'<span class="bt">{esc(s["title"])}</span><span class="bl">{label}</span></div>')


def question_grid(items, cls, start=1, numbered_prefix=""):
    cells = []
    for i, (q, _a) in enumerate(items, start):
        cells.append(
            f'<div class="q"><div class="qhead"><span class="qn">{numbered_prefix}{i}</span>'
            f'<span class="qq">{m(q)}</span></div>'
            f'<div class="work"></div><div class="ans"><span>=</span><span class="line"></span></div></div>')
    return f'<div class="qgrid {cls}">{"".join(cells)}</div>'


def cover():
    rows = "".join(
        f'<tr><td class="sn">{s["num"]}</td><td><b>{esc(s["title"])}</b><br>'
        f'<span class="small">{rich(s["can"])}</span></td>'
        f'<td class="tick">☐</td><td class="tick">☐</td><td class="score">&nbsp;&nbsp;&nbsp;&nbsp;/ 8</td></tr>'
        for s in C.SECTIONS)
    body = f"""
<div class="cover-top">
  <div class="cover-kicker">Basic Skills Booklet</div>
  <h1>{esc(C.TITLE)}</h1>
  <div class="cover-sub">{esc(C.SUBTITLE)}</div>
</div>
<div class="namebox">
  <div>Name: <span class="fill"></span></div>
  <div>Class: <span class="fill short"></span></div>
</div>

<h2>How to use this booklet</h2>
<div class="how">
  <div class="how-step"><div class="how-n">1</div><div><b>Learn</b><br>Read the notes and the worked
  examples. Each example shows every step.</div></div>
  <div class="how-step"><div class="how-n">2</div><div><b>Practise</b><br>Do <b>Practice A</b>, then
  <b>Practice B</b>. Check your answers at the back of the booklet and fix any mistakes.</div></div>
  <div class="how-step"><div class="how-n">3</div><div><b>Skill Check</b><br>When you're ready, do the
  Skill Check <b>on your own, without notes</b>. Your teacher will mark it.</div></div>
</div>

<h2>My progress</h2>
<table class="progress">
<tr><th></th><th>Skill</th><th>Practice A<br>done</th><th>Practice B<br>done</th><th>Skill Check<br><span class="small">(teacher)</span></th></tr>
{rows}
<tr class="total"><td></td><td><b>Mixed Review</b> (extra practice)</td><td class="tick" colspan="2">☐</td><td class="score">Total&nbsp;&nbsp;&nbsp;&nbsp;/ 40</td></tr>
</table>
<p class="small center">Tip: the answers to all the <b>practice</b> questions are at the back. The Skill Checks are not —
that's where you show what you can do!</p>
"""
    return page(body, "cover")


def learn_page(s):
    return page(section_banner(s, "Learn") + f'<div class="can">🎯 {rich(s["can"])}</div>'
                + f'<div class="learn">{rich(s["learn"])}</div>', "learn-page")


def practice_page(s, part, label, instr):
    items = s[part]
    cls = "wide" if s["id"] in ("expand", "factorise") else ""
    if len(items) <= 8:
        cls += " roomy"
    body = (section_banner(s, label)
            + f'<p class="instr">{esc(instr)} <span class="small">Show your working in the space.</span></p>'
            + question_grid(items, cls)
            + '<p class="check-note">✔ Check your answers at the back. Fix any you got wrong before moving on.</p>')
    return page(body, "practice-page")


def skill_check_page(s):
    cells = []
    for i, (q, _a) in enumerate(s["check"], 1):
        cells.append(
            f'<div class="sc"><div class="sc-head"><span class="qn">{i}</span>{m(q)}'
            f'<span class="markbox"></span></div><div class="sc-work"></div>'
            f'<div class="ans"><span>=</span><span class="line"></span></div></div>')
    body = f"""
{section_banner(s, "Skill Check")}
<div class="sc-top">
  <div>Name: <span class="fill"></span></div>
  <div class="teacher">Teacher mark:<span class="big-score"></span>/ 8</div>
</div>
<p class="instr"><b>{esc(C.CHECK_INSTRUCTIONS[s["id"]])}</b> Do this on your own — no notes.
Show your working. Write your final answer on the line.</p>
<div class="scgrid">{"".join(cells)}</div>
"""
    return page(body, "check-page")


def mixed_page():
    items = [(q, a) for _sec, q, a in C.MIXED]
    body = ('<div class="banner"><span class="bn">★</span><span class="bt">Mixed Review</span>'
            '<span class="bl">Extra practice</span></div>'
            '<p class="instr">A mix of all five skills. Look at each question carefully — which skill do you need? '
            '<span class="small">Answers are at the back.</span></p>'
            + question_grid(items, "wide mixed"))
    return page(body, "practice-page")


def answer_list(items, start=1):
    return "<ol class='alist' start='%d'>%s</ol>" % (
        start, "".join(f"<li>{m(a)}</li>" for _q, a in items))


def answers_pages():
    blocks = []
    for s in C.SECTIONS:
        blocks.append(
            f'<div class="ablock"><h3>{s["num"]}. {esc(s["title"])}</h3>'
            f'<div class="acols"><div><h4>Practice A</h4>{answer_list(s["practice_a"])}</div>'
            f'<div><h4>Practice B</h4>{answer_list(s["practice_b"])}</div></div></div>')
    mixed = [(q, a) for _s, q, a in C.MIXED]
    blocks.append(f'<div class="ablock"><h3>★ Mixed Review</h3>'
                  f'<div class="acols"><div>{answer_list(mixed[:10])}</div>'
                  f'<div>{answer_list(mixed[10:], 11)}</div></div></div>')
    body = ('<h2 class="ahead">Answers to the Practice Questions</h2>'
            '<p class="small">Terms can be in a different order and still be right — for example '
            f'{m("2b + 3a")} is the same as {m("3a + 2b")}, and {m("(x + 3)(x + 2)")} is the same as {m("(x + 2)(x + 3)")}.</p>'
            + "".join(blocks))
    return page(body, "answers-page")


CSS_LINK = '<link rel="stylesheet" href="booklet.css">'


def doc(title, pages):
    return f"""<!DOCTYPE html>
<html lang="en-NZ"><head><meta charset="utf-8"><title>{esc(title)}</title>{CSS_LINK}</head>
<body>{"".join(pages)}</body></html>
"""


def student_booklet():
    pages = [cover()]
    for s in C.SECTIONS:
        a_instr, b_instr = C.PRACTICE_INSTRUCTIONS[s["id"]]
        pages += [learn_page(s),
                  practice_page(s, "practice_a", "Practice A", a_instr),
                  practice_page(s, "practice_b", "Practice B", b_instr),
                  skill_check_page(s)]
    pages += [mixed_page(), answers_pages()]
    return doc(f"{C.TITLE} — Student Booklet", pages)


MARKING_NOTES = {
    "like-terms": "Accept terms in any order (e.g. 2b + 8a). The answer must be fully simplified (e.g. 3b, not b + 2b).",
    "multiply": "Accept letters in any order (e.g. 3ba). Q6–8 need the square: x × x = x², not 2x or x × x.",
    "divide": "Accept the answer written as a simplified fraction only if it has been fully cancelled (e.g. 4x, not 12x²/3x).",
    "expand": "Accept terms in any order. Q7–8: accept the unsimplified four-term answer (e.g. x² + 3x + 2x + 6) at your discretion as partial evidence; full mark needs the like terms collected.",
    "factorise": "Accept brackets in either order. Q4 must be fully factorised: 2(3y + 5). Students can check by expanding.",
}


def teacher_key():
    blocks = []
    for s in C.SECTIONS:
        rows = "".join(f"<tr><td>{i}</td><td>{m(q)}</td><td><b>{m(a)}</b></td></tr>"
                       for i, (q, a) in enumerate(s["check"], 1))
        blocks.append(
            f'<div class="kblock"><h3>Skill Check {s["num"]}: {esc(s["title"])} <span class="small">(8 marks, 1 per question)</span></h3>'
            f'<table class="key"><tr><th>Q</th><th>Question</th><th>Answer</th></tr>{rows}</table>'
            f'<p class="small"><b>Marking:</b> {esc(MARKING_NOTES[s["id"]])}</p></div>')
    key_page = page('<h1 class="khead">Teacher Answer Key — Skill Checks</h1>'
                    '<p>Each Skill Check is out of 8 (1 mark per question, for the correct final answer). '
                    'Record the mark in the box at the top of the Skill Check page and in the student\'s '
                    '<i>My progress</i> table on the cover. A suggested pass mark for each skill is <b>6 / 8</b>.</p>'
                    + "".join(blocks), "key-page")
    rec_rows = "".join("<tr>" + "<td></td>" * 7 + "</tr>" for _ in range(28))
    record = page('<h1 class="khead">Class Record</h1>'
                  '<table class="record"><tr><th>Student</th>'
                  + "".join(f"<th>{s['num']}. {esc(s['title'])}<br>/ 8</th>" for s in C.SECTIONS)
                  + "<th>Total<br>/ 40</th></tr>" + rec_rows + "</table>", "record-page")
    return doc(f"{C.TITLE} — Teacher Answer Key", [key_page, record, answers_pages()])


def main():
    n, errors = check_all()
    if errors:
        print("ANSWER CHECK FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"Checked {n} questions: every answer is correct, simplified and fully factorised.")
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "student-booklet.html"), "w") as f:
        f.write(student_booklet())
    with open(os.path.join(BUILD, "teacher-answer-key.html"), "w") as f:
        f.write(teacher_key())
    with open(os.path.join(os.path.dirname(__file__), "booklet.css")) as src, \
         open(os.path.join(BUILD, "booklet.css"), "w") as dst:
        dst.write(src.read())
    print("Wrote build/student-booklet.html and build/teacher-answer-key.html")


if __name__ == "__main__":
    main()

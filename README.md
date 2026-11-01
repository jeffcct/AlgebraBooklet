# Algebra Basic Skills Booklet

This is an easy, confidence-building booklet for students who need another go at five basic algebra skills. It is written in LaTeX.

**Print this:** `Algebra-Basic-Skills-Booklet.pdf` (16 A4 pages).

## What's inside

| Page | Contents |
|------|----------|
| 1 | Cover: title, name and class lines, and a **My progress** table for each skill's Skill Check mark (out of 4, 24 in total) |
| 2–13 | Two pages per skill: a **Learn** page (notes and 6 worked examples), then a **Practice** page with 12 questions that get a little harder as they go |
| 14–15 | **Skill Checks**: 4 questions for each skill, three skills per page, so they're easy to tear out and mark. There are name, mark and total boxes, and **no Skill Check answers appear anywhere** |
| 16 | Answers to the practice questions, so students can check their own work |

The six skills are:

1. Collecting like terms (a's, b's, x's, x²'s)
2. Multiplying algebra
3. Dividing algebra
4. Expanding single brackets, including negatives
5. Factorising into a single bracket
6. Substitution (replacing letters with numbers, including a few negative values)

## Editing

The questions and notes are in `src/content.py`. The notes are written in LaTeX, with maths in backticks. After editing, rebuild from the repository root:

```bash
python3 src/build.py
```

This first checks every practice answer: it must equal its question when tested at random values, and it must be fully simplified or factorised. If any answer is wrong, the build stops. It then writes `booklet/algebra-basic-skills.tex` and runs `pdflatex` to make the PDF. You need a TeX Live install with the `tcolorbox`, `enumitem`, `titlesec` and `fancyhdr` packages; on Debian/Ubuntu that is `texlive-latex-extra`.

The generated `.tex` file is also committed, so you can compile or tweak it directly. Changes made only in the `.tex` will be overwritten the next time `build.py` runs.

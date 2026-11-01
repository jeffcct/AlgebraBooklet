# Algebra Basic Skills Booklet

This is an easy, confidence-building booklet for students who need another go at five basic algebra skills. It is written in LaTeX.

**Print this:** `Algebra-Basic-Skills-Booklet.pdf` (24 A4 pages).

## What's inside

| # | Skill | Learn | Practice A | Practice B | Skill Check (teacher marks) |
|---|-------|-------|------------|------------|-----------------------------|
| 1 | Collecting like terms (a's, b's, x's, x²'s) | notes + 6 worked examples | 12 | 12 | 4 questions |
| 2 | Multiplying algebra | notes + 6 worked examples | 12 | 12 | 4 questions |
| 3 | Dividing algebra | notes + 6 worked examples | 12 | 12 | 4 questions |
| 4 | Expanding single brackets, including negatives | notes + 6 worked examples + sign rules | 12 | 12 | 4 questions |
| 5 | Factorising into a single bracket | notes + 6 worked examples | 12 | 12 | 4 questions |

- **Cover:** a "How to use this booklet" guide and a **My progress** table. The teacher writes each Skill Check score in it (out of 4 per skill, 20 in total).
- **Skill Checks:** one after each skill. Each has a name line, a "Teacher mark: / 4" box and a mark square for each question. **No Skill Check answers appear anywhere**: they are for the teacher to mark.
- **Mixed Review:** 20 more practice questions covering all five skills.
- **Answers to the practice questions** (not the Skill Checks) are at the back, so students can check their own work.

## Editing

The questions and notes are in `src/content.py`. The notes are written in LaTeX, with maths in backticks. After editing, rebuild from the repository root:

```bash
python3 src/build.py
```

This first checks every practice answer: it must equal its question when tested at random values, and it must be fully simplified or factorised. If any answer is wrong, the build stops. It then writes `booklet/algebra-basic-skills.tex` and runs `pdflatex` to make the PDF. You need a TeX Live install with the `tcolorbox`, `enumitem`, `titlesec` and `fancyhdr` packages; on Debian/Ubuntu that is `texlive-latex-extra`.

The generated `.tex` file is also committed, so you can compile or tweak it directly. Changes made only in the `.tex` will be overwritten the next time `build.py` runs.

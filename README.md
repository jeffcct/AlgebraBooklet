# Algebra Booklets

This repo has two printable LaTeX workbooks. Each one has the same layout:

- a cover with a progress table;
- two pages per skill: a **Learn** page, then a **Practice** page;
- **Skill Checks** at the back, which the teacher marks. No Skill Check answers appear anywhere;
- answers to the practice questions on the last page.

| Print this | For | Pages |
|------------|-----|-------|
| `Algebra-Basic-Skills-Booklet.pdf` | Students who need another go at the basics | 16 |
| `Algebra-Extension-Workbook.pdf` | Students who did reasonably well and need harder work | 16 |

## Basic Skills booklet

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

## Extension workbook

Six skills, chosen from what students found hard on the test:

1. **Factorising fully**: spotting the highest common factor, including letters, e.g. `12x + 36 = 12(x + 3)` (not `6(2x + 6)`) and `12x² + 30x = 6x(2x + 5)`.
2. **Substituting negatives**, e.g. `x² − 2x` when `x = −3`.
3. **Index laws**, including the "Liam says 3⁴ × 3² = 9⁶" question as a worked example, plus practice and Skill Check questions in the same style.
4. **Equations with brackets**, and writing equations from a story.
5. **Inequalities**: solving them (including flipping the sign) and showing the answer on a number line.
6. **Writing linear rules** from a table of values or from a story.

Each skill has 8–12 practice questions. The Skill Checks have 2–4 questions per skill, 18 marks in total.

## Editing

The questions and notes are in `src/content.py` (basic) and `src/content_extension.py` (extension). The notes are written in LaTeX, with maths in backticks. After editing, rebuild from the repository root:

```bash
python3 src/build.py
```

To build just one of them, add `basic` or `extension` to the end of that command.

This first checks every practice answer. Expressions must equal their question when tested at random values, and must be fully simplified or factorised. Equations, inequalities, tables and story rules are checked by substituting values. If any answer is wrong, the build stops. It then writes the `.tex` files in `booklet/` and runs `pdflatex` to make the PDFs. You need a TeX Live install with the `tcolorbox`, `enumitem`, `titlesec` and `fancyhdr` packages; on Debian/Ubuntu that is `texlive-latex-extra`.

The generated `.tex` files are also committed, so you can compile or tweak them directly. Changes made only in the `.tex` will be overwritten the next time `build.py` runs.

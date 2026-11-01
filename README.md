# Algebra Basic Skills Booklet

This is an easy, confidence-building booklet that re-teaches five basic algebra skills. It is for students who need another go at them after a test.

**Print these:**

- `Algebra-Basic-Skills-Booklet.pdf` is the student booklet (24 A4 pages).
- `Algebra-Basic-Skills-Teacher-Answer-Key.pdf` has the Skill Check answers, marking notes and a class record sheet. Don't hand it out to students.

## What's in the student booklet

| # | Skill | Learn | Practice A | Practice B | Skill Check (teacher marks) |
|---|-------|-------|------------|------------|-----------------------------|
| 1 | Collecting like terms (a's, b's, x's, x²'s) | notes + 6 worked examples | 12 | 12 | 8 marks |
| 2 | Multiplying algebra | notes + 6 worked examples | 12 | 12 | 8 marks |
| 3 | Dividing algebra | notes + 6 worked examples | 12 | 12 | 8 marks |
| 4 | Expanding brackets (single, then simple double) | notes + grid method | 12 | 8 | 8 marks |
| 5 | Factorising into brackets (common factor, then simple quadratics) | notes + "multiply/add" table | 12 | 8 | 8 marks |

- The cover page has a "How to use this booklet" guide and a **My progress** table. The teacher writes each Skill Check score (out of 8, total out of 40) there.
- A **Mixed Review** page has 20 more questions across all five skills.
- The **practice answers are at the back**, so students can check their own work. The Skill Check answers are **only** in the teacher key.
- The questions are kept easy. Practice A is one-step questions, and Practice B adds one small extra step. Every number in the double-bracket and quadratic questions is positive.

## Editing

All the text and questions are in `src/content.py`. To rebuild after editing, run these from the repository root:

```bash
python3 src/build.py
```

```bash
node src/make_pdf.js
```

`build.py` checks every answer before it builds anything. It tests each answer against its question at random values, and confirms the answer is simplified (or fully factorised). If any answer is wrong, it stops with an error. `make_pdf.js` uses Playwright/Chromium to print `build/*.html` to PDF.

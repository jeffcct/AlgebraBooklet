"""All booklet content: learning notes, practice questions, skill checks.

Maths is written in plain text inside backticks in the HTML notes, and as plain
strings in the question lists. build.py turns it into nicely typeset HTML:
  - letters become italic variables
  - ^2 becomes a superscript
  - '-' becomes a proper minus sign
Use × for multiply and ÷ for divide.

Every question is (question, answer). build.py checks every answer is
algebraically equal to its question before it builds anything.

Question "kinds" tell the checker how to compare:
  simplify  - the answer must equal the question expression
  factorise - same check, the question is the expanded form
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
    "learn": """
<p><b>Like terms</b> have <b>exactly the same letter part</b>. You can only add or
subtract like terms.</p>

<table class="like-table">
<tr><th>Like terms ✔</th><th>NOT like terms ✘</th></tr>
<tr><td>`3a` and `5a`</td><td>`3a` and `5b` (different letters)</td></tr>
<tr><td>`x` and `7x`</td><td>`x` and `7` (one has no letter)</td></tr>
<tr><td>`2x^2` and `x^2`</td><td>`x^2` and `x` (`x^2` is not the same as `x`)</td></tr>
<tr><td>`4ab` and `ab`</td><td>`ab` and `a`</td></tr>
</table>

<div class="tip"><b>Think of the letters as objects.</b>
3 apples + 4 apples = 7 apples, so `3a + 4a = 7a`.<br>
But 3 apples + 2 bananas is just 3 apples + 2 bananas, so `3a + 2b` stays as `3a + 2b`.</div>

<div class="tip"><b>A letter on its own means 1 of it.</b> `a` is the same as `1a`. So `a + a + a = 3a`.</div>

<h3>Worked examples</h3>
<div class="examples">
<div class="example"><div class="ex-q">`3a + 4a`</div>
<div class="ex-s">3 lots of `a` plus 4 lots of `a`</div>
<div class="ex-a">`= 7a`</div></div>

<div class="example"><div class="ex-q">`6x - 2x`</div>
<div class="ex-s">6 take away 2 is 4</div>
<div class="ex-a">`= 4x`</div></div>

<div class="example"><div class="ex-q">`5y - y`</div>
<div class="ex-s">`y` means `1y`, and 5 − 1 = 4</div>
<div class="ex-a">`= 4y`</div></div>

<div class="example"><div class="ex-q">`2a + 3b + 4a + b`</div>
<div class="ex-s">The `a`'s: `2a + 4a = 6a`<br>The `b`'s: `3b + b = 4b`</div>
<div class="ex-a">`= 6a + 4b`</div></div>

<div class="example"><div class="ex-q">`x^2 + 3x + 2x^2`</div>
<div class="ex-s">The `x^2`'s: `x^2 + 2x^2 = 3x^2`<br>The `x`'s: just `3x`</div>
<div class="ex-a">`= 3x^2 + 3x`</div></div>

<div class="example"><div class="ex-q">`7m + 2 - 3m`</div>
<div class="ex-s">The `m`'s: `7m - 3m = 4m`<br>The numbers: just `2`</div>
<div class="ex-a">`= 4m + 2`</div></div>
</div>

<div class="remember"><b>Remember:</b> the sign (+ or −) in <b>front</b> of a term belongs to that
term. Highlight or circle each type of term in a different colour before you add them up.</div>
""",
    "practice_a": [
        ("a + a", "2a"),
        ("a + a + a", "3a"),
        ("2a + 3a", "5a"),
        ("4x + 5x", "9x"),
        ("3m + m", "4m"),
        ("7b - 3b", "4b"),
        ("6y - y", "5y"),
        ("10x - 4x", "6x"),
        ("2p + 3p + p", "6p"),
        ("8c - 2c", "6c"),
        ("x^2 + x^2", "2x^2"),
        ("3x^2 + 4x^2", "7x^2"),
    ],
    "practice_b": [
        ("2a + 3b + 4a", "6a + 3b"),
        ("5x + 2y + x", "6x + 2y"),
        ("3a + 2b + a + 4b", "4a + 6b"),
        ("4x + 3 + 2x", "6x + 3"),
        ("7m - 2m + 3n", "5m + 3n"),
        ("5a + 2b - 3a", "2a + 2b"),
        ("6x + 4 - 2x + 1", "4x + 5"),
        ("8x - 3x + 2y", "5x + 2y"),
        ("4ab + 2ab", "6ab"),
        ("x^2 + 2x + 3x", "x^2 + 5x"),
        ("2x^2 + x + x^2", "3x^2 + x"),
        ("3y^2 + 2y + y^2 + 4y", "4y^2 + 6y"),
    ],
    "check": [
        ("4a + 3a", "7a"),
        ("9x - 5x", "4x"),
        ("b + b + b", "3b"),
        ("3a + 2b + 5a", "8a + 2b"),
        ("6x + 4y - 2x", "4x + 4y"),
        ("2x^2 + 5x^2", "7x^2"),
        ("x^2 + 4x + 3x", "x^2 + 7x"),
        ("3x^2 + 2x + x^2 + 5x", "4x^2 + 7x"),
    ],
}

# ---------------------------------------------------------------------------
# 2. Multiplying
# ---------------------------------------------------------------------------
MULTIPLY = {
    "id": "multiply",
    "num": 2,
    "title": "Multiplying Algebra",
    "can": "I can multiply terms, e.g. `2a × 3b = 6ab` and `x × x = x^2`",
    "kind": "simplify",
    "learn": """
<p>In algebra we <b>don't write the × sign</b>. Letters and numbers that are multiplied
are just written next to each other, <b>number first</b>.</p>

<table class="like-table">
<tr><th>We write…</th><th>…it means</th></tr>
<tr><td>`3a`</td><td>`3 × a`</td></tr>
<tr><td>`ab`</td><td>`a × b`</td></tr>
<tr><td>`5xy`</td><td>`5 × x × y`</td></tr>
<tr><td>`x^2`</td><td>`x × x` (say "x squared")</td></tr>
</table>

<div class="steps-box"><b>How to multiply terms</b>
<ol>
<li><b>Multiply the numbers</b> together.</li>
<li><b>Write the letters</b> after the number (in alphabetical order).</li>
<li>If the <b>same letter</b> appears twice, write it as a <b>square</b>: `x × x = x^2`.</li>
</ol></div>

<h3>Worked examples</h3>
<div class="examples">
<div class="example"><div class="ex-q">`4 × a`</div>
<div class="ex-s">Number first, then the letter</div>
<div class="ex-a">`= 4a`</div></div>

<div class="example"><div class="ex-q">`a × b`</div>
<div class="ex-s">Write the letters together</div>
<div class="ex-a">`= ab`</div></div>

<div class="example"><div class="ex-q">`2a × 4`</div>
<div class="ex-s">Numbers: 2 × 4 = 8<br>Letters: `a`</div>
<div class="ex-a">`= 8a`</div></div>

<div class="example"><div class="ex-q">`2a × 3b`</div>
<div class="ex-s">Numbers: 2 × 3 = 6<br>Letters: `a` and `b`</div>
<div class="ex-a">`= 6ab`</div></div>

<div class="example"><div class="ex-q">`x × x`</div>
<div class="ex-s">The same letter twice is "squared"</div>
<div class="ex-a">`= x^2`</div></div>

<div class="example"><div class="ex-q">`3x × 2x`</div>
<div class="ex-s">Numbers: 3 × 2 = 6<br>Letters: `x × x = x^2`</div>
<div class="ex-a">`= 6x^2`</div></div>
</div>

<div class="remember"><b>Remember:</b> when you <b>multiply</b>, the numbers multiply (`3 × 2 = 6`) —
don't add them! And `x × x` is `x^2`, not `2x`.<br>
<b>Going further:</b> `x × x × x = x^3` ("x cubed"), and `x^2 × x = x^3`.</div>
""",
    "practice_a": [
        ("4 × a", "4a"),
        ("5 × x", "5x"),
        ("a × b", "ab"),
        ("x × y", "xy"),
        ("2 × 3a", "6a"),
        ("3x × 4", "12x"),
        ("3 × 5m", "15m"),
        ("6 × 2x", "12x"),
        ("a × a", "a^2"),
        ("y × y", "y^2"),
        ("2a × b", "2ab"),
        ("p × q × r", "pqr"),
    ],
    "practice_b": [
        ("2a × 3b", "6ab"),
        ("4x × 2y", "8xy"),
        ("5a × 2b", "10ab"),
        ("2ab × 3", "6ab"),
        ("3a × a", "3a^2"),
        ("2x × 5x", "10x^2"),
        ("4m × 3m", "12m^2"),
        ("3x × 2x", "6x^2"),
        ("a × 2b × 3", "6ab"),
        ("x × x × x", "x^3"),
        ("x^2 × x", "x^3"),
        ("2x^2 × 3x", "6x^3"),
    ],
    "check": [
        ("3 × 4a", "12a"),
        ("m × n", "mn"),
        ("4x × 3", "12x"),
        ("a × 3b", "3ab"),
        ("2a × 5b", "10ab"),
        ("x × x", "x^2"),
        ("3y × 2y", "6y^2"),
        ("2x × 4x", "8x^2"),
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
    "learn": """
<p>Dividing is the opposite of multiplying. A division can also be written as a fraction:
`6a ÷ 2` is the same as <span class="frac"><span>`6a`</span><span>`2`</span></span>.</p>

<div class="steps-box"><b>How to divide terms</b>
<ol>
<li><b>Divide the numbers.</b></li>
<li><b>Cancel any letter</b> that is on the top <b>and</b> the bottom.</li>
<li>Write down what is left.</li>
</ol></div>

<div class="tip"><b>Why can letters cancel?</b> Anything divided by itself is 1. Just like `5 ÷ 5 = 1`,
`a ÷ a = 1`. So <span class="frac"><span>`ab`</span><span>`a`</span></span> = `b`.</div>

<h3>Worked examples</h3>
<div class="examples">
<div class="example"><div class="ex-q">`6a ÷ 2`</div>
<div class="ex-s">Numbers: 6 ÷ 2 = 3<br>Letters: `a` stays</div>
<div class="ex-a">`= 3a`</div></div>

<div class="example"><div class="ex-q">`ab ÷ a`</div>
<div class="ex-s">The `a` cancels<br>`b` is left</div>
<div class="ex-a">`= b`</div></div>

<div class="example"><div class="ex-q">`8x ÷ x`</div>
<div class="ex-s">The `x` cancels<br>8 is left</div>
<div class="ex-a">`= 8`</div></div>

<div class="example"><div class="ex-q">`12ab ÷ 4a`</div>
<div class="ex-s">Numbers: 12 ÷ 4 = 3<br>`a` cancels, `b` is left</div>
<div class="ex-a">`= 3b`</div></div>

<div class="example"><div class="ex-q">`x^2 ÷ x`</div>
<div class="ex-s">`x^2` is `x × x`<br>One `x` cancels, one is left</div>
<div class="ex-a">`= x`</div></div>

<div class="example"><div class="ex-q">`6x^2 ÷ 3x`</div>
<div class="ex-s">Numbers: 6 ÷ 3 = 2<br>Letters: `x^2 ÷ x = x`</div>
<div class="ex-a">`= 2x`</div></div>
</div>

<div class="remember"><b>Remember:</b> if <b>all</b> the letters cancel you are left with just a
number, e.g. `5a ÷ a = 5`. Write `x^2` as `x × x` if it helps you see what cancels.</div>
""",
    "practice_a": [
        ("8a ÷ 2", "4a"),
        ("12x ÷ 3", "4x"),
        ("10b ÷ 5", "2b"),
        ("20y ÷ 4", "5y"),
        ("9x ÷ 3", "3x"),
        ("15p ÷ 5", "3p"),
        ("18x ÷ 9", "2x"),
        ("6m ÷ 6", "m"),
        ("ab ÷ b", "a"),
        ("xy ÷ x", "y"),
        ("5a ÷ a", "5"),
        ("7x ÷ x", "7"),
    ],
    "practice_b": [
        ("6ab ÷ 2a", "3b"),
        ("12xy ÷ 4y", "3x"),
        ("10ab ÷ 5b", "2a"),
        ("8xy ÷ 2x", "4y"),
        ("14ab ÷ 7", "2ab"),
        ("x^2 ÷ x", "x"),
        ("a^2 ÷ a", "a"),
        ("4x^2 ÷ x", "4x"),
        ("6x^2 ÷ 2x", "3x"),
        ("15a^2 ÷ 5a", "3a"),
        ("20x^2 ÷ 4x", "5x"),
        ("9x^2 ÷ 3x", "3x"),
    ],
    "check": [
        ("10a ÷ 2", "5a"),
        ("16x ÷ 4", "4x"),
        ("xy ÷ y", "x"),
        ("9a ÷ a", "9"),
        ("8ab ÷ 4a", "2b"),
        ("y^2 ÷ y", "y"),
        ("12x^2 ÷ 3x", "4x"),
        ("20ab ÷ 5b", "4a"),
    ],
}

# ---------------------------------------------------------------------------
# 4. Expanding brackets
# ---------------------------------------------------------------------------
EXPAND = {
    "id": "expand",
    "num": 4,
    "title": "Expanding Brackets",
    "can": "I can expand brackets, e.g. `3(x + 2) = 3x + 6`",
    "kind": "simplify",
    "learn": """
<p><b>Expanding</b> means getting rid of the brackets by multiplying.
A number or letter right in front of a bracket means <b>multiply everything inside</b> the bracket by it.</p>

<h3>Part 1: One bracket</h3>
<div class="steps-box"><b>Multiply the outside by EVERY term inside.</b> Draw arrows so you don't miss one!
<div class="arrow-demo">`3(x + 2)`&nbsp;&nbsp;→&nbsp;&nbsp;`3 × x` and `3 × 2`&nbsp;&nbsp;→&nbsp;&nbsp;`3x + 6`</div></div>

<div class="examples">
<div class="example"><div class="ex-q">`4(a + 5)`</div>
<div class="ex-s">`4 × a = 4a`<br>`4 × 5 = 20`</div>
<div class="ex-a">`= 4a + 20`</div></div>

<div class="example"><div class="ex-q">`2(x - 3)`</div>
<div class="ex-s">`2 × x = 2x`<br>`2 × 3 = 6`, keep the minus</div>
<div class="ex-a">`= 2x - 6`</div></div>

<div class="example"><div class="ex-q">`x(x + 5)`</div>
<div class="ex-s">`x × x = x^2`<br>`x × 5 = 5x`</div>
<div class="ex-a">`= x^2 + 5x`</div></div>
</div>

<h3>Part 2: Two brackets</h3>
<p>Everything in the first bracket multiplies everything in the second bracket.
A <b>grid</b> makes it easy to keep track. Example: `(x + 2)(x + 3)`</p>
<div class="grid-wrap">
<table class="grid">
<tr><th>×</th><th>`x`</th><th>`+3`</th></tr>
<tr><th>`x`</th><td>`x^2`</td><td>`3x`</td></tr>
<tr><th>`+2`</th><td>`2x`</td><td>`6`</td></tr>
</table>
<div class="grid-notes">
<p>1. Put one bracket on top and one down the side.</p>
<p>2. Multiply to fill each box.</p>
<p>3. Add up all four boxes: `x^2 + 3x + 2x + 6`</p>
<p>4. Collect the like terms in the middle:</p>
<p class="big">`(x + 2)(x + 3) = x^2 + 5x + 6`</p>
</div></div>

<div class="remember"><b>Remember:</b> the outside term multiplies <b>every</b> term inside —
`3(x + 2)` is `3x + 6`, <b>not</b> `3x + 2`. With two brackets, you should always get <b>4</b> boxes.</div>
""",
    "practice_a": [
        ("2(x + 3)", "2x + 6"),
        ("3(a + 4)", "3a + 12"),
        ("5(x + 1)", "5x + 5"),
        ("6(x + 2)", "6x + 12"),
        ("4(y - 2)", "4y - 8"),
        ("2(m - 5)", "2m - 10"),
        ("3(2x + 1)", "6x + 3"),
        ("2(4a + 3)", "8a + 6"),
        ("5(2y - 1)", "10y - 5"),
        ("x(x + 2)", "x^2 + 2x"),
        ("a(a + 5)", "a^2 + 5a"),
        ("x(x - 3)", "x^2 - 3x"),
    ],
    "practice_b": [
        ("(x + 1)(x + 2)", "x^2 + 3x + 2"),
        ("(x + 3)(x + 4)", "x^2 + 7x + 12"),
        ("(x + 2)(x + 5)", "x^2 + 7x + 10"),
        ("(x + 1)(x + 6)", "x^2 + 7x + 6"),
        ("(x + 2)(x + 4)", "x^2 + 6x + 8"),
        ("(x + 5)(x + 1)", "x^2 + 6x + 5"),
        ("(x + 3)(x + 3)", "x^2 + 6x + 9"),
        ("(x + 4)(x + 5)", "x^2 + 9x + 20"),
    ],
    "check": [
        ("4(x + 2)", "4x + 8"),
        ("3(a - 5)", "3a - 15"),
        ("2(3x + 1)", "6x + 2"),
        ("5(2a + 3)", "10a + 15"),
        ("x(x + 7)", "x^2 + 7x"),
        ("y(y - 4)", "y^2 - 4y"),
        ("(x + 2)(x + 3)", "x^2 + 5x + 6"),
        ("(x + 1)(x + 4)", "x^2 + 5x + 4"),
    ],
}

# ---------------------------------------------------------------------------
# 5. Factorising
# ---------------------------------------------------------------------------
FACTORISE = {
    "id": "factorise",
    "num": 5,
    "title": "Factorising into Brackets",
    "can": "I can factorise, e.g. `2x + 6 = 2(x + 3)`",
    "kind": "factorise",
    "learn": """
<p><b>Factorising</b> is the <b>opposite of expanding</b>. We put the brackets back in.</p>
<div class="arrow-demo center">`2(x + 3)` &nbsp;&nbsp;— expand →&nbsp;&nbsp; `2x + 6`
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `2x + 6` &nbsp;&nbsp;— factorise →&nbsp;&nbsp; `2(x + 3)`</div>

<h3>Part 1: Take out a common factor</h3>
<div class="steps-box"><ol>
<li>Find the <b>biggest number</b> (and/or <b>letter</b>) that goes into <b>both</b> terms.
    Write it outside the bracket.</li>
<li><b>Divide</b> each term by it. Write the answers inside the bracket.</li>
<li><b>Check</b> by expanding — you should get back to the question.</li>
</ol></div>

<div class="examples">
<div class="example"><div class="ex-q">`5a + 10`</div>
<div class="ex-s">5 goes into both<br>`5a ÷ 5 = a`, `10 ÷ 5 = 2`</div>
<div class="ex-a">`= 5(a + 2)`</div></div>

<div class="example"><div class="ex-q">`6x - 9`</div>
<div class="ex-s">3 goes into both<br>`6x ÷ 3 = 2x`, `9 ÷ 3 = 3`</div>
<div class="ex-a">`= 3(2x - 3)`</div></div>

<div class="example"><div class="ex-q">`x^2 + 4x`</div>
<div class="ex-s">`x` goes into both<br>`x^2 ÷ x = x`, `4x ÷ x = 4`</div>
<div class="ex-a">`= x(x + 4)`</div></div>
</div>

<h3>Part 2: Two brackets</h3>
<p>To factorise `x^2 + 5x + 6`, find <b>two numbers</b> that
<b>multiply</b> to the last number (6) and <b>add</b> to the middle number (5).</p>
<div class="grid-wrap">
<table class="pairs">
<tr><th>Multiply to 6</th><th>Add to…</th></tr>
<tr><td>1 × 6</td><td>1 + 6 = 7 ✘</td></tr>
<tr class="hit"><td>2 × 3</td><td>2 + 3 = 5 ✔</td></tr>
</table>
<div class="grid-notes">
<p>The two numbers are 2 and 3, so they go in the brackets:</p>
<p class="big">`x^2 + 5x + 6 = (x + 2)(x + 3)`</p>
<p>Check by expanding: `(x + 2)(x + 3) = x^2 + 3x + 2x + 6 = x^2 + 5x + 6` ✔</p>
</div></div>

<div class="remember"><b>Remember:</b> always <b>check by expanding</b> your answer. The brackets
can go in either order: `(x + 3)(x + 2)` is also correct.</div>
""",
    "practice_a": [
        ("3x + 6", "3(x + 2)"),
        ("2a + 8", "2(a + 4)"),
        ("5x + 15", "5(x + 3)"),
        ("7m + 7", "7(m + 1)"),
        ("4y - 12", "4(y - 3)"),
        ("2x - 10", "2(x - 5)"),
        ("6a + 9", "3(2a + 3)"),
        ("10x + 15", "5(2x + 3)"),
        ("x^2 + 3x", "x(x + 3)"),
        ("a^2 + 5a", "a(a + 5)"),
        ("x^2 - 2x", "x(x - 2)"),
        ("y^2 + y", "y(y + 1)"),
    ],
    "practice_b": [
        ("x^2 + 3x + 2", "(x + 1)(x + 2)"),
        ("x^2 + 4x + 3", "(x + 1)(x + 3)"),
        ("x^2 + 6x + 8", "(x + 2)(x + 4)"),
        ("x^2 + 5x + 4", "(x + 1)(x + 4)"),
        ("x^2 + 7x + 10", "(x + 2)(x + 5)"),
        ("x^2 + 7x + 12", "(x + 3)(x + 4)"),
        ("x^2 + 8x + 15", "(x + 3)(x + 5)"),
        ("x^2 + 6x + 9", "(x + 3)(x + 3)"),
    ],
    "check": [
        ("4x + 8", "4(x + 2)"),
        ("5m + 5", "5(m + 1)"),
        ("3a - 9", "3(a - 3)"),
        ("6y + 10", "2(3y + 5)"),
        ("x^2 + 6x", "x(x + 6)"),
        ("a^2 - 4a", "a(a - 4)"),
        ("x^2 + 5x + 6", "(x + 2)(x + 3)"),
        ("x^2 + 6x + 5", "(x + 1)(x + 5)"),
    ],
}

SECTIONS = [LIKE_TERMS, MULTIPLY, DIVIDE, EXPAND, FACTORISE]

# Instructions shown at the top of each practice set
PRACTICE_INSTRUCTIONS = {
    "like-terms": ("Simplify by collecting like terms.", "Simplify by collecting like terms. Some have two types of term."),
    "multiply": ("Simplify.", "Simplify. Watch for the same letter twice!"),
    "divide": ("Simplify.", "Simplify. Cancel the letters that are on top and bottom."),
    "expand": ("Expand.", "Expand and simplify. Use the grid to help."),
    "factorise": ("Factorise.", "Factorise into two brackets."),
}
CHECK_INSTRUCTIONS = {
    "like-terms": "Simplify by collecting like terms.",
    "multiply": "Simplify.",
    "divide": "Simplify.",
    "expand": "Expand (and simplify where needed).",
    "factorise": "Factorise fully.",
}

# Mixed review: one section number + question/answer each, so it can be checked too.
MIXED = [
    (1, "5a + 2a", "7a"),
    (2, "3 × 2x", "6x"),
    (3, "12y ÷ 3", "4y"),
    (4, "2(x + 5)", "2x + 10"),
    (5, "3x + 12", "3(x + 4)"),
    (1, "4x + 3y + 2x", "6x + 3y"),
    (2, "a × 4b", "4ab"),
    (3, "10ab ÷ 2b", "5a"),
    (4, "x(x + 1)", "x^2 + x"),
    (5, "x^2 + 7x", "x(x + 7)"),
    (1, "8m - 3m", "5m"),
    (2, "5x × x", "5x^2"),
    (3, "6x^2 ÷ x", "6x"),
    (4, "4(2a - 1)", "8a - 4"),
    (5, "5y - 20", "5(y - 4)"),
    (1, "2x^2 + 3x + x^2", "3x^2 + 3x"),
    (2, "4a × 2a", "8a^2"),
    (3, "16xy ÷ 8x", "2y"),
    (4, "(x + 1)(x + 3)", "x^2 + 4x + 3"),
    (5, "x^2 + 4x + 4", "(x + 2)(x + 2)"),
]

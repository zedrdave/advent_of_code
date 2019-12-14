# Advent of code 2019

See https://adventofcode.com/2019/about

* To run Python code (when `<DAY>/__main__.py` is present): `python3 -m 2019.<DAY>` **from the repo root**
* If you have Pipenv: `pipenv run python3 -m 2019.<DAY>`, from the repo root (will automatically install all dependencies)
* To run standalone `.py` code: `python3 ./FILE.py`
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`
* to run `.go` code: `go build -o out.exe FILE.go && ./out.exe` (or simply: `go run FILE.go`)

OCaml fans: [right this way](https://github.com/regnat/aoc-2019)…

## 1

Ideal job for Python + `numpy` with vectorisation.

Didn't initially check for negative vals. Turned out there weren't any, but probably not good practice.

Part 1 was a simpler version of [the Tyranny of the Rocket Equation](https://www.nasa.gov/mission_pages/station/expeditions/expedition30/tryanny.html) (minus fuel exhaustion). I think it even gets a mention in [XKCD's What If](https://what-if.xkcd.com) book version…

Part 2 could probably be solved using arithmetico-geometric series convergence (though dealing with `floor` would be a pain).

**Today's lesson:** Recursion is fun.

### 2

Guess who's got two thumbs and wasted 10 mins by failing to read the last line of instructions… 👈😑🤟

Good reminder that good coding starts with reading the specs well.

Wondering if there's a more convoluted but nicer way to solve part 2, than brute-forcing. Something about deconstructing all the opcodes and identifying all params pointing to `0`?

Also went full [Arbitrary Condiment](https://www.xkcd.com/974/), with an alternate [2_2_bis.c](https://github.com/zedrdave/advent_of_code/blob/master/2019/02/2_2_bis.c) version that could handle arbitrary opcodes.

Solved Part 2 in Python, then dusted off gcc to see if it looked nicer (it doesn't, but I suspect it might, if there start being a richer opcode grammar).

For the sake of it, I added all necessary checks in the C code, but I reckon size could be halved by just relying on correctly formed input.

**Today's lesson:** Read *all* the specs.

## 3

Went with detecting intersections between two sets of segments (restricted to vertical or horizontal).

Thought that foregoing binary-tree sweep search implementation was already total brute-force, then watched [this guy's 5 mins solution](https://www.youtube.com/watch?v=tMPQp60q9GA) and realised how hilariously off-base I was. There is indeed no good reason to deal with continuous-plane segments, rather than using the discrete grid nature of the problem, and exhaustively listing all points (wouldn't scale for larger input/grid size, but who cares).

Decidedly not a natural competitive-coder here. (but still a valuable lesson in the dangers of overthinking and premature optimisation)

Before solving Part 2: made code clearer, life easier and bugs rarer, by implementing a quick wrapper class `Point(x, y)`… Then remembered that `[collections.namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)` existed (FFS: `Point` is even the doc's example).

**TIL** that `x1 < y < x2` is perfectly good Python, and indeed equivalent to `x1 < y and y < x2` as one would hope/expect (obvious in retrospect).

Can easily optimise by adding: `if step_counts and s1_steps + s2_steps > min(step_counts): continue`, but lose the ability to debug the process.

**Today's lesson:** Stop solving *general* (continous plane), when *specific* (discrete grid) is so much easier to solve.

## 4

Very uninspired bruteforcing. Neither concise nor elegant, and didn't have the time to revisit with something nicer.

Had I realised that the monotony conditions ensured only one `d+` pattern match (eg no `113311` or `134156`) would have greatly simplified the counting problem!

Favourite solution (not mine):
```
check = lambda n: list(n) == sorted(n) and 2 in map(n.count, n)
sum(check(str(n)) for n in range(123456, 654321))
```

**Today's lesson:** Take a breath and try again.

## 5

My [arbitrary condiment version of day 2](https://github.com/zedrdave/advent_of_code/blob/master/2019/02/2_2_bis.c) turned out to be useful after all, and not arbitrary enough. Silly restrictions like:
* Fixed-sized opcodes
* Opcodes only able to affect instruction pointer relative to current position

… both made life harder for Day 5.

Did a [clean rewrite](https://github.com/zedrdave/advent_of_code/blob/master/2019/02/2_2_bis.c) that now uses a global IP (and memory buffer), allowing ops to do pretty much anything (I'm sure I'll be proven wrong on that at some future date). Initially went hogwild with macros, then chose clarity over concision, and used proper functions.

**TIL**: C ternary operator is *not* a macro (duh), and therefore: `(a ? b : c) = 1` does not compile (depending on compiler, it might compile to something useless).

**Today's lesson:** Thinking ahead sometimes pays off.

## 6

Expecting part 2 to be a bit more solid, I went straight to a graph lib, with `networkx`. Code took a couple minutes (after spending 10 mins realising I had not used any graph lib in 2 years, did not remember any, googling around, and figuring out how to use it).

Turns out it works just fine with a [basic `dict` of node parents](https://github.com/zedrdave/advent_of_code/blob/master/2019/06/6b.py). But something tells me more serious graphs will make a comeback.

**Today's lesson:** Stop overthinking.

## 7

> "There is no way [using all these global vars](https://github.com/zedrdave/advent_of_code/blob/master/2019/05/5_2.c) could ever come back and bite me in the aaaaaaa…"

Was immediately obvious that my "design choices" (ie laziness) on Day 5 were going to make today's code [hideously painful](https://github.com/zedrdave/advent_of_code/blob/master/2019/07/7_2.c).

With the stars out of the way, I did take the time for a [quick rewrite in C++](https://github.com/zedrdave/advent_of_code/blob/master/2019/07/7.cpp) (objects, or at least struct, seem self-evident here). Dropped the function pointers (doable, but just didn't feel like spending the time brushing up on C++ method pointers).

And then, for comparison (and also, let's be honest: future use), I did a [quick rewrite in Python](https://github.com/zedrdave/advent_of_code/blob/master/2019/07/7.py).

Looking at the near-exact identical implementations in C++ and Python, makes me realise why I haven't written a line of C++ in years. [Programming is fun again](https://www.xkcd.com/353/).

**Today's lesson:** Globals are *evil*.

## 8

A gentle Sunday-friendly 5-line refresher in Numpy array manipulations.

… which I decided to turn into a [ridiculously overblown version](https://github.com/zedrdave/advent_of_code/blob/master/2019/08/8_ML.py) that creates and trains a Machine Learning model (with Keras) to identify each bitmap character and output its text equivalent.

* Its only assumptions, are an input made of 6x5 px uppercase letters (it originally looked for separations, but turns out some chars are touching each other).
* The code generates its own training set using available fonts. Due to cross-platform limitations, finding any univeersal monospaced fonts was a PITA… I finally gave up and added open-sourced fonts to the package.
* The training set generation also uses scaled down versions of multiple sizes, to add some variability.
* Running the code with pipenv (`pipenv run python 8_ML.py`) should automatically install all needed packages before running.

**Today's lesson:** Machine Learning is fun!

## 9

Another nice and easy one (thanks to my Python rewrite). Woke up much earlier than usual and started at 6:35am (questions open at 6am local time), but still not enough to crack the top 1000.

With this addition, I believe Intcode can now execute subroutines… I am tempted to rewrite Day 7's permutation optimisation, into one single Intcode program.

**Today's lesson:** Python makes everything better.

## 10

Grid/pathfinder problems are clearly my blind spot (don't encounter many of these in real life work).

First time I had to leave halfway through (after a laborious silver star) to go to work. After a bit of fresh air, some coffee and time to think, it turned out the solution was fairly simple (GCD for the win). Highlight of that day: realising I literally do not remember even the most basic trig, and taking 5 mins to convert negative angles to positive.

**Today's lesson:** Trigonometry is sometimes useful.

## 11

Mostly an opportunity for some code cleanup:
* Moved Intcode's `VM` to its own module (now requires running with `python3 -m`. See above).
* Packed a few useful functions into a `utils` module
* Created a standalone `utils.OCR` class, with the ML OCR reader from Day 8
* Turned Intcode `VM`'s main function (`run`) into a generator, that `yield` output values…

And with all these changes, I was able to rewrite my original [very raw solution](https://github.com/zedrdave/advent_of_code/blob/master/2019/11/11.py) into a neat concise bit of code that not only solves the problem rather elegantly, but also uses OCR to predict the text output from the bitmap…

One major change from my initial code: using a sparse matrix, rather than allocating a ridiculously large `numpy.array` and hoping the program would remain within bounds. Turns out I did not even need `scipy.sparse`, as a mere `defaultdict(int)` with tuple keys works beautifully…

**Today's lesson:** Use sparsity, Luke.

## 12

Straightfoward numpy stuff (could be done with native python lists, but I really did not want to trade numpy vectorised operations for a clusterfest of list comprehensions).

Part 2 stumped me for a solid 2 minutes, at which point I decided to go for my morning shower and coffee. After which, obvious trick (treat each dimension separately) became clear as day.

**Today's lesson:** When stuck: go for a coffee break.

## 13

An absolutely awesome extension of Intcode…

Share of time spent trying to solve Part 2:

* Playing Breakout to get final score: **50 mins**
* Looking for brick-to-points pattern: **15 mins**
* Disassembling Intcode score increment routine: **20 mins** (gave up halfway there)
* Implementing look-ahead-based auto-play: **10 mins** 😑

When thinking about the easiest way to implement auto-play, I briefly considered a follow-the-ball heuristic, but (erraneously) assumed that this might not always be enough to catch the ball. Instead, I took advantage of Intcode nice little self-contained VM, to run a look-ahead each time the ball is hit by the paddle. Overkill as usual, but I quite like it, since a similar approach could be used to implement some sophisticated heuristics (eg where multiple options need to be analysed each time).

For **interactive mode**: I struggled a bit with reading arrow chars from Python's `sys.stdin.read()`, and ended up mapping letters instead. It also turns out that Curses does not play well with double-char unicode emojis (no nice colourful output).

**Today's lesson:** *Breakout* is hard. But fun!

## 14

Starting to get the hang of that "do not overcomplicate" thing: just as I was about to create a DAG of reactions (because of course you need to take into account multiple ways to produce the same element), I ran a quick Counter on all the products, and realised they were all unique. Simple `product -> reactants` dict was more than enough.

I *did* attempt a brute-force for Part 2, stopped after 20s… and implemented a quick bisection method, as any sane person would.

**Today's lesson:** `O(log n)`, bitch.

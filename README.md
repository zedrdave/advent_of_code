# Advent of code 2019

See https://adventofcode.com/2019/about

* To run `.py` code: `python3 ./FILE.py`
* To run `.py` with necessary modules (when a `Pipfile` is present): `pipenv run python ./FILE.py`
* To run `<DAY>/__main__.py` code: `python3 -m advent_of_code_2019.<DAY>` **from the directory above `advent_of_code_2019`** (runs as a module)
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`
* to run `.go` code: `go build -o out.exe FILE.go && ./out.exe` (or simply: `go run FILE.go`)

OCaml fans: [right this way](https://github.com/regnat/aoc-2019)…

## 1
### 1.1

Ideal job for Python + `numpy` with vectorisation. Might be a tad more compact in `R`.

Didn't initially check for negative vals. Turned out there weren't any, but probably not good practice.

### 1.2

Simpler version of [the Tyranny of the Rocket Equation](https://www.nasa.gov/mission_pages/station/expeditions/expedition30/tryanny.html) (minus fuel exhaustion). I think it even gets a mention in [XKCD's What If](https://what-if.xkcd.com) book version…

Can probably be solved using arithmetico-geometric series convergence (though dealing with the `floor` would be a pain).

## 2

Solved it in Python, then dusted off gcc to see if it looked nicer (it doesn't, but I suspect it might, if there start being a richer opcode grammar).

For the sake of it, I added all necessary checks in the C code, but I reckon size could be halved by just relying on correctly formed input.

### 2.1

Guess who's got two thumbs and wasted 10 mins by failing to read the last line of instructions… 👈😑🤟

Good reminder that good coding starts with reading the specs well.

### 2.2

Wondering if there's a more convoluted but nicer way to solve, than brute-forcing. Something about deconstructing all the opcodes and identifying all params pointing to `0`?

Also went full [Arbitrary Condiment](https://www.xkcd.com/974/), with an alternate [2_2_bis.c](https://github.com/zedrdave/advent_of_code_2019/blob/master/02/2_2_bis.c) version that could handle arbitrary opcodes.

## 3

### 3.1

Went with detecting intersections between two sets of segments (restricted to vertical or horizontal).

Thought that foregoing binary-tree sweep search implementation was already total brute-force, then watched [this guy's 5 mins solution](https://www.youtube.com/watch?v=tMPQp60q9GA) and realised how hilariously off-base I was. There is indeed no good reason to deal with continuous-plane segments, rather than using the discrete grid nature of the problem, and exhaustively listing all points (wouldn't scale for larger input/grid size, but who cares).

Decidedly not a natural competitive-coder here. (but still a valuable lesson in the dangers of overthinking and premature optimisation)

### 3.2

Made code clearer, life easier and bugs rarer, by implementing a quick wrapper class `Point(x, y)`: dealing with `p.x`/`p.y` rather than `p[0]`/`p[1]`…

**TIL** that `x1 < y < x2` is perfectly good Python, and indeed equivalent to `x1 < y and y < x2` as one would hope/expect (obvious in retrospect).

Can easily optimise by adding: `if step_counts and s1_steps + s2_steps > min(step_counts): continue`, but lose the ability to debug the process.

## 4

Very uninspired bruteforcing. Neither concise nor elegant, and didn't have the time to revisit with something nicer.

Had I realised that the monotony conditions ensured only one `d+` pattern match (eg no `113311` or `134156`) would have greatly simplified the counting problem!

Favourite solution (not mine):
```
check = lambda n: list(n) == sorted(n) and 2 in map(n.count, n)
sum(check(str(n)) for n in range(123456, 654321))
```

## 5

My [arbitrary condiment version of day 2](https://github.com/zedrdave/advent_of_code_2019/blob/master/02/2_2_bis.c) turned out to be useful after all, and not arbitrary enough. Silly restrictions like:
* Fixed-sized opcodes
* Opcodes only able to affect instruction pointer relative to current position

… both made life harder for Day 5.

Did a [clean rewrite](https://github.com/zedrdave/advent_of_code_2019/blob/master/02/2_2_bis.c) that now uses a global IP (and memory buffer), allowing ops to do pretty much anything (I'm sure I'll be proven wrong on that at some future date). Initially went hogwild with macros, then chose clarity over concision, and used proper functions.

**TIL**: C ternary operator is *not* a macro (duh), and therefore: `(a ? b : c) = 1` does not compile (depending on compiler, it might compile to something useless).


## 6

Expecting part 2 to be a bit more solid, I went straight to a graph lib, with `networkx`. Code took a couple minutes (after spending 10 mins realising I had not used any graph lib in 2 years, did not remember any, googling around, and figuring out how to use it).

Turns out it works just fine with a [basic `dict` of node parents](https://github.com/zedrdave/advent_of_code_2019/blob/master/06/6b.py). But something tells me more serious graphs will make a comeback.

## 7

> "There is no way [using all these global vars](https://github.com/zedrdave/advent_of_code_2019/blob/master/05/5_2.c) could ever come back and bite me in the aaaaaaa…"

Was immediately obvious that my "design choices" (ie laziness) on Day 5 were going to make today's code [hideously painful](https://github.com/zedrdave/advent_of_code_2019/blob/master/07/7_2.c).

With the stars out of the way, I did take the time for a [quick rewrite in C++](https://github.com/zedrdave/advent_of_code_2019/blob/master/07/7.cpp) (objects, or at least struct, seem self-evident here). Dropped the function pointers (doable, but just didn't feel like spending the time brushing up on C++ method pointers).

And then, for comparison (and also, let's be honest: future use), I did a [quick rewrite in Python](https://github.com/zedrdave/advent_of_code_2019/blob/master/07/7.py).

Looking at the near-exact identical implementations in C++ and Python, makes me realise why I haven't written a line of C++ in years. [Programming is fun again](https://www.xkcd.com/353/).

## 8

A gentle Sunday-friendly 5-line refresher in Numpy array manipulations.

… which I decided to turn into a [ridiculously overblown version](https://github.com/zedrdave/advent_of_code_2019/blob/master/08/8_ML.py) that creates and trains a Machine Learning model (with Keras) to identify each bitmap character and output its text equivalent.

* Its only assumptions, are an input made of 6x5 px uppercase letters (it originally looked for separations, but turns out some chars are touching each other).
* The code generates its own training set using available fonts. Due to cross-platform limitations, finding any univeersal monospaced fonts was a PITA… I finally gave up and added open-sourced fonts to the package.
* The training set generation also uses scaled down versions of multiple sizes, to add some variability.
* Running the code with pipenv (`pipenv run python 8_ML.py`) should automatically install all needed packages before running.

## 9

Another nice and easy one. Woke up much earlier than usual and started at 6:35am (questions open at 6am local time), but still not enough to crack the top 1000.

With this addition, I believe Intcode can now execute subroutines… I am tempted to rewrite Day 7's permutation optimisation, into one single Intcode program.

## 10

Mostly an opportunity for some code cleanup:
* Moved Intcode's `VM` to its own module (now requires running with `python3 -m`. See above).
* Packed a few useful functions into a `utils` module
* Created a standalone `utils.OCR` class, with the ML OCR reader from Day 8
* Turned Intcode `VM`'s main function (`run`) into a generator, that `yield` output values…

And with all these changes, I was able to rewrite my original [very raw solution](https://github.com/zedrdave/advent_of_code_2019/blob/master/11/11.py) into a neat concise bit of code that not only solves the problem rather elegantly, but also uses OCR to predict the text output from the bitmap…

One major change from my initial code: using a sparse matrix, rather than allocating a ridiculously large `numpy.array` and hoping the program would remain within bounds. Turns out I did not even need `scipy.sparse`, as a mere `defaultdict(int)` with tuple keys works beautifully…

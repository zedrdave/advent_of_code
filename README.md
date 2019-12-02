# Advent of code 2019

See https://adventofcode.com/2019/about

* To run `.py` code: `python3 ./FILE.py`
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`

Personal notes:

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

ALso went full [Arbitrary Condiment](https://www.xkcd.com/974/), with an alternate `2_2_bis.c` version that could handle arbitrary opcodes.

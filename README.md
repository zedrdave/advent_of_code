# Advent of code 2019

See https://adventofcode.com/2019/about

Personal notes:

## 1

### 1.1

Didn't initially check for negative vals. Turned out there weren't any, but probably not good practice.

### 1.2

Simpler version of (the Tyranny of the Rocket Equation)[https://www.nasa.gov/mission_pages/station/expeditions/expedition30/tryanny.html] (minus fuel exhaustion).

Can probably be solved using arithmetico-geometric series convergence (though dealing with the `floor` would be a pain).

## 2

Definitely better solved in a compiler-friendly language like C, but was too lazy to dust off my raw gcc skills.

### 2.1

Guess who's got two thumbs and wasted 10 mins by failing to read the last line of instruction and omitting init values… 👈😑🤟

Good reminder that good coding starts with reading the specs well.

### 2.2

Wondering if there's a more convoluted but nicer way to solve, than brute-forcing. Something about deconstructing all the opcodes and identifying all params pointing to `0`?

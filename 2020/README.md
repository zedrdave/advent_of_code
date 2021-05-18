# Advent of code 2020

See https://adventofcode.com/2020/about

* To run Python code: `python3 -m 2020.<DAY>` **from the repo root**
* *Optional* (if you have Pipenv installed): `pipenv run python3 -m 2020.<DAY>`
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`
* to run `.go` code: `go build -o out.exe FILE.go && ./out.exe` (or simply: `go run FILE.go`)


This year's self-imposed challenge was "tweet-sized" solutions (in Python). That is: solutions that fit in 280 bytes (input loading and result output included), all the while preserving readability as much as humanly possible (ie: no code-golfing). Mostly succeeded, save for one or two days that just wouldn't fit without resorting to unacceptable code-mangling: https://github.com/zedrdave/advent_of_code/blob/master/2020/Tweets.ipynb


## 1

Straightforward Day 1 opener.

With input size `n = 200`, there really was no need overthink it past a brute-force loop (too lazy to even break out `itertools` doc).

For those who *did* want to optimise, there's an [elegant solution](https://gist.github.com/sharpobject/72ccfe8eaac07346576fb5e6670681da) using a lookup table to bring complexity down from `O(n^r)` to `O(n^ceil(r/2))` (with `r` the number of digits to add/multiply).

## 2

Still very straightforward territory.

Because I never learn, I wasted a good 5 out of 10 mins, screwing around with regex and fancy search functions that I *knew* weren't necessary, before deciding to settle for a simple, clean, list comprehension: `[x == c for c in mystring]`…


## 3

Not gonna lie: I *knew* `mod` was the way to go. But I also knew that merely repeating the grid a bunch of times would work fine and spare my sleep-deprived neurones a teeny bit of work at 6am (did eventually clean up the code).

## 4

Buncha Regexes and fairly mundane validation exercise (yay for functional languages).

## 5

Some fun at last. Slightly ashamed that it took me until the beginning of the second part, to bother noticing that there was no need to split row bits and col bits to compute the seat id.

*TiL* that a `int(x, base)` could be used to quickly convert a string of binaries (but due to the need to replace each character, list comprehension weren't a bad idea anyway).

## 6

Zzz. Counters are great, I suppose?

Might have been a tad more interesting to solve using `itertools`

## 7

More string parsing and counting…

## 8

Be still, my heart: Intcode v.2!

After getting a quick-and-dirty brute-force solution out of the way, used `networkx` to optimally search for and fix the program cycle. Doubt it will be a useful implementation for possible future re-use of this interpreter, but still fun.

## 9

Starting to get a little disappointed by the ability to brute-force all the problems so far…

## 10

"Here we go again, I'm sure nothing a quick brute-force recursion won't s…" ⏳⌛️⏳⌛️

Since I got up way past leaderboard-making time, I decided to skip the quick solution (using DP/memoization) and instead fell down the rabbit-hole of analysing the input structure to find the "trick" (this is probably where being a veteran of AoC 2019 helped: that Part 1 was way too specific not to be a hint). Which turned out to be [a lot more fun than expected](https://github.com/zedrdave/advent_of_code/blob/master/2020/10/__main__.py):

1. Sort and pad the input
1. Compute diffs between adjacent items (thanks to Part 1, we know these diffs are only 1 or 3)
1. Break down the input into sub-lists of consecutive numbers separated by numbers that can't be removed (diff == 3).
1. Realise that these sub-lists can be renumbered to simple `range(n)`, WLOG
1. Solve the *much easier* problem of "How many binary strings of length `n` where `000` does not appear"
1. Manually compute that value for small `n`: `0,1,1,2,4,7,13,24` 
1. If you are smart (I'm not): plop it into a [search engine](https://duckduckgo.com/?q=1%2C1%2C2%2C4%2C7%2C13%2C24%2C44&t=osx&ia=web) or better yet, directly into [OES](https://oeis.org/A000073).
1. If you aren't smart-enough, but driven: toy around with the recursive formula until you realise you are dealing with `F(n) = F(n-3) + F(n-2) + F(n-1)`, aka the [Tribonacci sequence](https://oeis.org/A000073).
1. Waste a bit of time playing with the idea of implementing a closed-form calculator of Tribonacci numbers, until you realise that a. an iterative approach is actually faster b. you barely need the first 5-6 to solve your input (so basically could have stopped at step 5)
1. 😎
1. Bask in the glory of having written a solution that runs in 94 µs instead of 328 µs.
1. Wonder why you are behind on your actual dayjob today.

*TIL*: Python has native support for operations on complex numbers: `a = 2 + 4j; b = a**2`.

## 11

Straightforward grid problem. Remembered how many grid problems last year were easily solvable with a sparse array as a simple Python dict and, sure enough: this one could be solved that way. Compact code, but *very* inefficient solving (`O(n^2)` per iteration, compared to `O(n)` for a basic grid implementation).

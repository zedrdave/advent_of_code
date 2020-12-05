# Advent of code 2020

See https://adventofcode.com/2020/about

* To run Python code: `python3 -m 2020.<DAY>` **from the repo root**
* *Optional* (if you have Pipenv installed): `pipenv run python3 -m 2020.<DAY>`
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`
* to run `.go` code: `go build -o out.exe FILE.go && ./out.exe` (or simply: `go run FILE.go`)


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

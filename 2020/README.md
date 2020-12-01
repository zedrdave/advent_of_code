# Advent of code 2019

See https://adventofcode.com/2020/about

* To run Python code: `python3 -m 2020.<DAY>` **from the repo root**
* *Optional* (if you have Pipenv installed): `pipenv run python3 -m 2019.<DAY>`
* To run `.c` code: `gcc FILE.c -o out.exe && ./out.exe`
* to run `.go` code: `go build -o out.exe FILE.go && ./out.exe` (or simply: `go run FILE.go`)


## 1

Straightforward Day 1 opener.

With input size `n = 200`, there really was no need overthink it past a brute-force loop (too lazy to even break out `itertools` doc).

For those who *did* want to optimise, there's an [elegant solution](https://gist.github.com/sharpobject/72ccfe8eaac07346576fb5e6670681da) using a lookup table to bring complexity down from `O(n^r)` to `O(n^ceil(r/2))` (with `r` the number of digits to add/multiply).

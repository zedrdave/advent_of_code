package main

import ("fmt"; "strings"; "io/ioutil")

func main() {
  contents, _ := ioutil.ReadFile("input.txt")
  orbits := strings.Split(strings.TrimSpace(string(contents)), "\n")

  // Build tree (map of all parents)
  parents := make(map[string] string)
  for _, orbit := range orbits {
    pair := strings.Split(orbit, ")")
    parents[pair[1]] = pair[0]
  }

  // Part 1
  tot := 0
  for n := range parents {
    tot += len(ancestors(parents, n))
  }
  fmt.Println("Part 1:", tot)

  // Part 2
  you_path := ancestors(parents, "YOU")
  santa_path := ancestors(parents, "SAN")

  // path between YOU and SAN is sum of paths to root - paths in common
  for i, item := range you_path {
    if santa_path[i] != item {
      fmt.Println("Part 2:", len(you_path) + len(santa_path) - 2*i)
      break
    }
  }
}

func ancestors(parents map[string] string, n string) []string {
  if parent, ok := parents[n]; ok {
    return append(ancestors(parents, parent), parent)
  } else {
    return make([]string, 0)
  }
}

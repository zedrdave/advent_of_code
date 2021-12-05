fn parse_input(input: &str) -> Vec<u16> {
    let mut coords: Vec<u16> = vec![];
    let mut num: String = String::new();

    for c in input.chars() {
        if c.is_ascii_digit() {
            num.push(c);
        } else if num.len() > 0 {
            coords.push(num.parse::<u16>().unwrap());
            num = String::new();
        }
    }
    coords.push(num.parse::<u16>().unwrap());
    coords
}

fn range(a: u16, b: u16) -> Vec<u16> {
    if a <= b {
        (a..(b + 1)).collect()
    } else {
        (b..(a + 1)).rev().collect()
    }
}

fn main() {
    let input = include_str!("../../input.txt");
    let coords = parse_input(input);

    use itertools::Itertools;
    use std::collections::HashMap;

    let mut grid: HashMap<(u16, u16), u16> = HashMap::new();
    for (x1, y1, x2, y2) in coords.clone().into_iter().tuples() {
        if x1 == x2 {
            for y in range(y1, y2) {
                *grid.entry((x1, y)).or_insert(0) += 1;
            }
        } else if y1 == y2 {
            for x in range(x1, x2) {
                *grid.entry((x, y1)).or_insert(0) += 1;
            }
        }
    }
    println!("Part 1: {}", grid.values().filter(|v| (**v) > 1).count());

    for (x1, y1, x2, y2) in coords
        .into_iter()
        .tuples()
        .filter(|(x1, y1, x2, y2)| x1 != x2 && y1 != y2)
    {
        for (&x, y) in range(x1, x2).iter().zip(range(y1, y2)) {
            *grid.entry((x, y)).or_insert(0) += 1;
        }
    }
    println!("Part 2: {}", grid.values().filter(|v| (**v) > 1).count());
}

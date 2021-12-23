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

fn main() {
    let input = include_str!("../../input.txt");
    let coords = parse_input(input);

    // use itertools::Itertools;
    // use std::collections::HashMap;

    println!("Part 1: {}", grid.values().filter(|v| (**v) > 1).count());
}

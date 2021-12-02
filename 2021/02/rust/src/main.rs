fn read_file_iter(filename: &str) -> impl Iterator<Item = (char, u32)> {
    use std::fs::File;
    use std::io::{BufRead, BufReader};
    BufReader::new(File::open(filename).unwrap())
        .lines()
        .map(|line| {
            let l = line.unwrap();
            let items = l.split_once(' ');
            (
                items.unwrap().0.chars().nth(0).unwrap(),
                items.unwrap().1.parse::<u32>().unwrap(),
            )
        })
}

fn main() {
    let mut data = read_file_iter("../input.txt");

    let mut horiz = 0;
    let mut depth = 0;

    for (cmd, val) in data {
        match cmd {
            'f' => horiz += val,
            'd' => depth += val,
            'u' => depth -= val,
            _ => println!("Unknown command: {}", cmd),
        }
    }
    println!("Part 1: {}", horiz * depth);

    data = read_file_iter("../input.txt");
    horiz = 0;
    depth = 0;
    let mut aim = 0;

    for (cmd, val) in data {
        match cmd {
            'f' => { horiz += val; depth += aim*val },
            'd' => aim += val,
            'u' => aim -= val,
            _ => println!("Unknown command: {}", cmd),
        }
    }
    println!("Part 2: {}", horiz * depth);

}

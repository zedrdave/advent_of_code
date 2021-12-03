fn read_file(filename: &str) -> Vec<Vec<u8>> {
    use std::fs::File;
    use std::io::{BufRead, BufReader};
    BufReader::new(File::open(filename).unwrap())
        .lines()
        .map(|line| {
            line.unwrap()
                .chars()
                .map(|c| ((c as u8) - 48))
                .collect::<Vec<u8>>()
        })
        .collect::<Vec<Vec<u8>>>()
}

fn least_most(sums: &Vec<u16>, data_len: u16, least: bool) -> u32 {
    sums.iter()
        .map(|i| i > &(data_len / 2))
        .rev()
        .enumerate()
        .fold(0, |accum, (i, b)| {
            if b ^ least {
                accum + u32::pow(2, i as u32)
            } else {
                accum
            }
        })
}

fn main() {
    let data = read_file("../input.txt");
    let sums: Vec<u16> = data.iter().fold(vec![0; data[0].len()], |mut accum, v| {
        for (a, b) in accum.iter_mut().zip(v.iter()) {
            *a += *b as u16;
        }
        accum
    });

    let most = least_most(&sums, data.len() as u16, false);
    let least = least_most(&sums, data.len() as u16, true);

    println!("Part 1: {}", (most * least));
}

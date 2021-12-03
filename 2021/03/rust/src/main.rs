fn read_file(filename: &str) -> Vec<Vec<u8>> {
    use std::fs::File;
    use std::io::{BufRead, BufReader};
    BufReader::new(File::open(filename).unwrap())
        .lines()
        .map(|line| {
            line.unwrap()
                .chars()
                .map(|c| (c as u8 - 48))
                .collect::<Vec<u8>>()
        })
        .collect::<Vec<Vec<u8>>>()
}

fn least_most(sums: &Vec<u16>, data_len: u16, least: bool) -> u32 {
    sums.iter()
        .map(|i| i > &(data_len / 2))
        .fold(0, |accum, b| accum * 2 + (b ^ least) as u32)
}

fn sieve(data: &Vec<Vec<u8>>, least: bool) -> u32 {
    let mut candidates: Vec<Vec<u8>> = data.clone();

    for i in 0..candidates[0].len() {
        let sum: u32 = candidates.iter().fold(0, |accum, v| (accum + v[i] as u32));
        let bit_criteria = (2 * sum < (candidates.len() as u32)) as bool ^ least;

        candidates = candidates
            .into_iter()
            .filter(|v| (v[i] != 0) == bit_criteria)
            .collect();

        if candidates.len() == 1 {
            break;
        };
    }

    candidates[0]
        .iter()
        .fold(0, |accum, b| accum * 2 + (*b as u32))
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
    println!("Part 2: {}", sieve(&data, false) * sieve(&data, true));
}

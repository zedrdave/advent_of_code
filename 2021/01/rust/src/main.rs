use itertools::izip;
use std::fs;

fn read_ints(filename: &str) -> Vec<u32> {
    fs::read_to_string(filename)
        .expect("Something went wrong reading input")
        .split("\n")
        .map(|x| x.parse::<u32>().unwrap())
        .collect::<Vec<u32>>()
}

// fn read_ints_iter(filename: &str) -> impl Iterator<Item = &u32> {
//     let str_data: String =
//         fs::read_to_string(filename).expect("Something went wrong reading input");
//     let myvec = str_data
//         .split("\n")
//         .map(|x| x.parse::<u32>().unwrap())
//         .collect::<Vec<u32>>();

//     return myvec.iter().clone();
// }

fn count_increases(data: &Vec<u32>) -> u32 {
    data.iter()
        .zip(data[1..].iter())
        .map(|(a, b)| (b > a) as u32)
        .sum::<u32>()
}

fn main() {
    let data = read_ints("../input.txt");
    println!("Part 1: {}", count_increases(&data));

    let triplets = izip!(data.iter(), data[1..].iter(), data[2..].iter())
        .map(|(a, b, c)| a + b + c)
        .collect::<Vec<u32>>();
    println!("Part 2: {:?}", count_increases(&triplets))
}

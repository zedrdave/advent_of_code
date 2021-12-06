// fn read_file(filename: &str) -> Vec<String> {
//     use std::fs::File;
//     use std::io::{BufRead, BufReader};
//     BufReader::new(File::open(filename).unwrap())
//         .read()
//         .map(|line| {
//             line.unwrap()
//                 .chars()
//                 .map(|c| (c as u8 - 48))
//                 .collect::<Vec<u8>>()
//         })
//         .collect::<Vec<Vec<u8>>>()
// }

// fn main() {
//     let data = read_file("../input.txt");

//     println!("Part 1: {}", data[0]);
// }

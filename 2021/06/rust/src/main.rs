fn count_fish_deque(init: &Vec<u64>, days: u32) -> u64 {
    use std::collections::VecDeque;

    let mut deq = VecDeque::from(init.clone());
    for _ in 0..days {
        let spawn = deq.pop_front().unwrap();
        // Is this the most efficient way to get deq[-2]:
        let save = deq.pop_back().unwrap();
        *deq.back_mut().unwrap() += spawn;
        deq.push_back(save);
        deq.push_back(spawn);
    }
    deq.iter().sum()
}

fn count_fish_vec(init: &Vec<u64>, days: u32) -> u64 {
    let mut fish = init.clone();
    let mut cur_idx: usize = 0;
    let l = fish.len();
    for _ in 0..days {
        fish[if cur_idx >= 2 {
            cur_idx - 2
        } else {
            l + cur_idx - 2
        }] += fish[cur_idx];
        cur_idx = (cur_idx + 1) % l;
    }
    fish.iter().sum()
}

use std::time::Instant;

fn main() {
    let mut input = vec![0; 9];
    for d in include_str!("../../input.txt")
        .split(',')
        .map(|d| d.parse::<usize>().unwrap())
    {
        input[d] += 1;
    }

    println!("Part 1: {}", count_fish_vec(&input, 80));
    println!("Part 2: {}", count_fish_vec(&input, 256));
    assert_eq!(count_fish_deque(&input, 256), count_fish_vec(&input, 256));

    // Benchmarking:
    let before = Instant::now();
    let n = 10000;
    for _ in 0..n {
        count_fish_deque(&input, 256);
    }
    println!("Deque version: {:.2?}", before.elapsed() / n);

    let before = Instant::now();
    let n = 10000;
    for _ in 0..n {
        count_fish_vec(&input, 256);
    }
    println!("Vec version: {:.2?}", before.elapsed() / n);
}

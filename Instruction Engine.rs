use std::{io, vec};

fn main() {
    let mut input_ = String::new();
    let mut reg_a: i32 = 0;
    loop {
        println!("> ");
        io::stdin().read_line(&mut input_).expect("Failed to read line!");
        let mut runthrough: Vec<&str> = input_.split_whitespace().collect();

        if runthrough[0] == "add" {
            if runthrough[1] == "a," {
                let mut number = runthrough[2].trim().parse::<i32>().unwrap();
                reg_a = reg_a + number;
                println!("added!");
            }
        }

        else if runthrough[0] == "print" {
            let mut temp_print = &runthrough[1..].join(" ");
            println!("{}", temp_print);
        }

    runthrough.clear();
    input_.clear();
    }

}

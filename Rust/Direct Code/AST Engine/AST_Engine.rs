use std::{io, vec};
use std::fs;
use std::time::Duration;
use std::thread;

fn main() {
    // Init
    let mut input_ = String::new();
    let mut reg_a: i32 = 0;

    // This small block of code handles file path input. The file path, I recommend, should be done with \\ and not /.
    println!("Program Path> ");
    io::stdin().read_line(&mut input_).expect("Failed to read path!");
    let filepath = input_.trim().to_string();
    let mut program: Result<String, io::Error> = fs::read_to_string(&filepath);

    // Full Body Loop
    loop {

        // This match extracts the String from the Result<>, because it's the only way we can split reliably for execution.
        // You can't really split a possibility.
        match program {

            // If string, do interpreter execution.
            // The for loop could be replaced with a while len pointer, but for current exec it's fine.
            Ok(value) => {

            // This splits the program into manageable strings for exec.
            let mut split_program: Vec<&str> = value.split(" ; ").collect();

            // Exec
            for item in split_program {
                let mut runthrough: Vec<&str> = item.split_whitespace().collect();

                // Each if/else if block here represents another instruction. Basically, each block is one part of syntax that can be manipulated.
                // Have fun with that!
                if runthrough[0] == "add" {
                    if runthrough[1] == "a," {
                        let mut number = runthrough[2].trim().parse::<i32>().unwrap();
                        reg_a = reg_a + number;
                        println!("added!");
                    }
                }

                // Print statement. It takes all words after the word print, as long as the first word is print.
                else if runthrough[0] == "print" {
                    let mut temp_print = &runthrough[1..].join(" ");
                    println!("{}", temp_print);
                }

                // Simple sleeping, good for debug.
                else if runthrough[0] == "sleep" {
                    let seconds = runthrough[1].parse::<u64>().unwrap();
                    thread::sleep(Duration::from_secs(seconds));
                }

            // Essentially, this clears the current queue of command so the next one can be run and no garbage is executed.
            // I learned this the hard way with print statements. *sigh*
            runthrough.clear();
                }
            }

            // This is for covering errors in program reading. If this shows up, either you chose a wrong file path or something is wrong with your code.
            Err(value) => {
                println!("Error reading program!")
            }
        }
    }
}

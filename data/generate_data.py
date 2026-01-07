import random
import json
import argparse
import os
from utils import apply_format, invert_string

def balanced_sampling(max_digits):
    """
    Sample d from [2, max_digits].
    Sample n1, n2 from [10^(d-1), 10^d - 1].
    """
    d = random.randint(2, max_digits)
    min_val = 10**(d-1)
    max_val = 10**d - 1
    n1 = random.randint(min_val, max_val)
    n2 = random.randint(min_val, max_val)
    return n1, n2, d

def random_sampling(max_digits):
    """
    Sample n1, n2 from [0, 10^max_digits - 1].
    """
    max_val = 10**max_digits - 1
    n1 = random.randint(0, max_val)
    n2 = random.randint(0, max_val)
    length = len(str(max(n1, n2)))
    return n1, n2, length

def generate_dataset(num_samples, max_digits, sampling_strategy, format, output_file, print_example=False, only_addition=False, inverse_input=False, inverse_output=False):
    if (num_samples <= 0):
        return

    data = []
    formats = ["decimal", "character", "fixed-character", "underscore", "words", "10-based", "10e-based"]
    if only_addition:
        operations = ["plus"]
    else:
        operations = ["plus", "minus"]

    # If format is invalid, choose random
    if (format not in formats):
        format = random.choice(formats)
    fmt = format

    for _ in range(num_samples):
        if sampling_strategy == "balanced":
            n1, n2, length = balanced_sampling(max_digits)
        else:
            n1, n2, length = random_sampling(max_digits)

        # Randomly choose between 2 operations
        op = random.choice(operations)

        if op == "plus":
            result = n1 + n2
            op_str = "plus"
        else:
            result = n1 - n2
            op_str = "minus"

        # Input: "What is [n1] [op] [n2]?"
        # Now change format for n1 and n2.
        
        s1 = apply_format(n1, fmt, max_digits)
        s2 = apply_format(n2, fmt, max_digits)
        s_res = apply_format(result, fmt, max_digits)
        
        # Invert input
        if inverse_input:
            s1 = invert_string(s1, fmt)
            s2 = invert_string(s2, fmt)
        
        # Example of changed format
        # Input: "What is 3 10e1 2 10e0 plus 5 10e0?"
        # Desired Result: "3 10e1 7 10e0"
        
        input_text = f"What is {s1} {op_str} {s2}?"
        target_text = s_res
        
        if inverse_output:
             target_text = invert_string(target_text, fmt)

        data.append({
            "input": input_text,
            "target": target_text,
            "format": fmt,
            "operation": op_str,
            "length": length
        })

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} \"{sampling_strategy}\" samples to {output_file}")

    if print_example:
        rng = random.randint(0, len(data) - 1) 
        print(f"\nOne random example:")
        print(f"Input: {data[rng]['input']}")
        print(f"Target: {data[rng]['target']}")
        print(f"Format: {data[rng]['format']}")
        print(f"Operation: {data[rng]['operation']}")
        print(f"Length: {data[rng]['length']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Common arguments
    parser.add_argument("--digits", type=int, default=6)
    parser.add_argument("--format", type=str, default="decimal")
    parser.add_argument("--print", type=bool, default=False)
    parser.add_argument("--only_addition", action="store_true", help="Only generate addition (remove subtraction)")
    parser.add_argument("--inverse-input", action="store_true", help="Reverse numbers in input")
    parser.add_argument("--inverse-output", action="store_true", help="Reverse the result")
    
    # Mode selection
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--mode", type=str, choices=["batch", "single", "experiment"], default="batch",
                        help="batch: Create 3 sets train/test/val. single: Create 1 custom set. experiment: Generate data for main experiment.")
    
    # Batch mode arguments
    parser.add_argument("--train", type=int, default=1000, help="[Batch / Experiment] Number of training samples")
    parser.add_argument("--test", type=int, default=1000, help="[Batch / Experiment] Number of test samples")
    parser.add_argument("--val", type=int, default=0, help="[Batch / Experiment] Number of val samples")

    # Single mode arguments
    parser.add_argument("--count", type=int, help="[Single] Number of samples")
    parser.add_argument("--strategy", type=str, choices=["balanced", "random"], help="[Single] Sampling rule")
    parser.add_argument("--output", type=str, help="[Single] Output file path")

    # Experiment mode arguments
    parser.add_argument("--base_path", type=str, default="data/experiment", help="[Experiment] Output directory")
    parser.add_argument("--digit_steps", type=int, nargs='+', default=None, help="[Experiment] List of max digits (default: 2, 5, 10, 15, 20, 25, 30)")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.mode == "experiment":
        # Main Experiment:
        # 5 sets of 1,000 addition samples (Balanced)
        # x-axis: max digits (e.g. 5, 10, 15, 20, 25, 30)
        # Validation set: 1,000 samples
        
        if args.digit_steps:
            digit_steps = args.digit_steps
        else:
            digit_steps = [2, 5, 10, 15, 20, 25, 30]
        
        print(f"Generating Experiment Data in {args.base_path}...")
        
        for d in digit_steps:
            # Create folder for each digit count
            dir_path = os.path.join(args.base_path, f"digits_{d}")
            os.makedirs(dir_path, exist_ok=True)
            
            print(f"  -> Processing {d} digits...")

            # Loop through 5 random seeds
            for run_id in range(1, 6):
                # Set base seed
                if args.seed is not None:
                    run_seed = args.seed + run_id
                    random.seed(run_seed)
                
                print(f"    -> Run {run_id}...")

                # 1. Train Set (Balanced, 1000 samples)
                train_file = os.path.join(dir_path, f"train_{run_id}.json")
                generate_dataset(1000, d, "random", args.format, train_file, only_addition=args.only_addition, inverse_input=args.inverse_input, inverse_output=args.inverse_output)

                # 2. Validation Set (Balanced, 1000 samples)
                val_file = os.path.join(dir_path, f"val_{run_id}.json")
                generate_dataset(1000, d, "random", args.format, val_file, only_addition=args.only_addition, inverse_input=args.inverse_input, inverse_output=args.inverse_output)

                # 3. Test Set (Random, 2000 samples)
                test_file = os.path.join(dir_path, f"test_{run_id}.json")
                generate_dataset(2000, d, "random", args.format, test_file, only_addition=args.only_addition, inverse_input=args.inverse_input, inverse_output=args.inverse_output)

    elif args.mode == "single":
        if not args.count or not args.strategy or not args.output:
            parser.error("Must provide --count, --strategy, and --output in single mode.")
        
        generate_dataset(
            num_samples=args.count,
            max_digits=args.digits,
            sampling_strategy=args.strategy,
            format=args.format,
            output_file=args.output,
            print_example=args.print,
            only_addition=args.only_addition,
            inverse_input=args.inverse_input,
            inverse_output=args.inverse_output
        )
    else:
        # Generate in batch mode
        # Create training data (Balanced)
        generate_dataset(
          num_samples=args.train, 
          max_digits=args.digits, 
          sampling_strategy="balanced", 
          format=args.format, 
          output_file="data/data_train.json", 
          print_example=args.print,
          only_addition=args.only_addition,
          inverse_input=args.inverse_input,
          inverse_output=args.inverse_output
        )

        # Create test data (Random)
        generate_dataset(
          num_samples=args.test, 
          max_digits=args.digits, 
          sampling_strategy="random", 
          output_file="data/data_test.json", 
          print_example=args.print,
          only_addition=args.only_addition,
          inverse_input=args.inverse_input,
          inverse_output=args.inverse_output
        )

        # Create validation data (Balanced, IF NEEDED)
        if (args.val > 0):
            generate_dataset(
                num_samples=args.val, 
                max_digits=args.digits, 
                sampling_strategy="balanced", 
                format=args.format, 
                output_file="data/data_val.json", 
                print_example=args.print,
                only_addition=args.only_addition,
                inverse_input=args.inverse_input,
                inverse_output=args.inverse_output
            )

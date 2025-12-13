import random
import json
import argparse
import os
from utils import apply_format

def balanced_sampling(max_digits):
    """
    Lấy mẫu d từ [2, max_digits].
    Lấy mẫu n1, n2 từ [10^(d-1), 10^d - 1].
    """
    d = random.randint(2, max_digits)
    min_val = 10**(d-1)
    max_val = 10**d - 1
    n1 = random.randint(min_val, max_val)
    n2 = random.randint(min_val, max_val)
    return n1, n2, d

def random_sampling(max_digits):
    """
    Lấy mẫu n1, n2 từ [0, 10^max_digits - 1].
    """
    max_val = 10**max_digits - 1
    n1 = random.randint(0, max_val)
    n2 = random.randint(0, max_val)
    length = len(str(max(n1, n2)))
    return n1, n2, length

def generate_dataset(num_samples, max_digits, sampling_strategy, format, output_file, print_example=False):
    if (num_samples <= 0):
        return

    data = []
    formats = ["decimal", "character", "fixed-character", "underscore", "words", "10-based", "10e-based"]
    operations = ["plus", "minus"]

    # Nếu format không hợp lệ, chọn ngẫu nhiên
    if (format not in formats):
        format = random.choice(formats)
    fmt = format

    for _ in range(num_samples):
        if sampling_strategy == "balanced":
            n1, n2, length = balanced_sampling(max_digits)
        else:
            n1, n2, length = random_sampling(max_digits)

        # Chọn ngẫu nhiên giữa 2 toán tử
        op = random.choice(operations)

        if op == "plus":
            result = n1 + n2
            op_str = "plus"
        else:
            result = n1 - n2
            op_str = "minus"

        # Đầu vào: "What is [n1] [op] [n2]?"
        # Giờ thì thay đổi định dạng cho n1 và n2.
        
        s1 = apply_format(n1, fmt, max_digits)
        s2 = apply_format(n2, fmt, max_digits)
        s_res = apply_format(result, fmt, max_digits)
        
        # Ví dụ đã thay đổi định dạng
        # Đầu vào: "What is 3 10e1 2 10e0 plus 5 10e0?"
        # Kết quả mong muốn: "3 10e1 7 10e0"
        
        input_text = f"What is {s1} {op_str} {s2}?"
        target_text = s_res

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

    # Số lượng mẫu huấn luyện
    parser.add_argument("--train", type=int, default=10000)

    # Số lượng mẫu kiểm tra
    parser.add_argument("--test", type=int, default=1000)

    # Số lượng mẫu validation (nếu cần)
    parser.add_argument("--val", type=int, default=0)

    # Số lượng chữ số tối đa
    parser.add_argument("--digits", type=int, default=6)

    # Định dạng
    parser.add_argument("--format", type=str, default="decimal")

    # In ra một ví dụ (nếu cần kiểm tra lại)
    parser.add_argument("--print", type=bool, default=False)
    args = parser.parse_args()

    # ========================================== CÁCH CHẠY FILE ========================================== # 
    # py generate_data.py --train 10000 --test 1000 --val 1000 --digits 6 --format [FORMAT]                #
    # Thêm --print True nếu muốn in ra một ví dụ                                                           #
    # CHỌN FORMAT TRONG: [decimal, character, fixed-character, underscore, words, 10-based, 10e-based]     #
    # ==================================================================================================== #

    # Tạo dữ liệu huấn luyện (Cân bằng)
    generate_dataset(
      num_samples=args.train, 
      max_digits=args.digits, 
      sampling_strategy="balanced", 
      format=args.format, 
      output_file="data/data_train.json", 
      print_example=args.print
    )

    # Tạo dữ liệu kiểm tra (Ngẫu nhiên)
    generate_dataset(
      num_samples=args.test, 
      max_digits=args.digits, 
      sampling_strategy="random", 
      format=args.format, 
      output_file="data/data_test.json", 
      print_example=args.print
    )

    # Tạo dữ liệu validation (Cân bằng, NẾU CẦN)
    if (args.val > 0):
        generate_dataset(
            num_samples=args.val, 
            max_digits=args.digits, 
            sampling_strategy="balanced", 
            format=args.format, 
            output_file="data/data_val.json", 
            print_example=args.print
        )

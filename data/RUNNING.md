# 💻 CÁCH CHẠY generate_data.py 💻

Script này hỗ trợ 2 chế độ (mode): `batch` (mặc định) và `single`.

## 1. Các tham số chung

- `--digits`: Số lượng chữ số tối đa của mẫu (mặc định: 6).
- `--format`: Định dạng của mẫu (mặc định: decimal).
- `--print`: In ra ví dụ mẫu sau khi tạo (mặc định: False).
- `--only_addition`: Chỉ tạo các phép tính cộng (loại bỏ phép trừ).
- `--mode`: Chế độ chạy (`batch` hoặc `single`).

## 2. Chế độ BATCH (Mặc định)

Tạo ra các tập dữ liệu `train`, `test` (và tùy chọn `val`) với tên file mặc định trong thư mục `data/`.

- Tập train: lấy mẫu cân bằng (balanced).
- Tập test: lấy mẫu ngẫu nhiên (random).

### Tham số riêng:

- `--train`: Số lượng mẫu huấn luyện (mặc định: 10000).
- `--test`: Số lượng mẫu kiểm tra (mặc định: 1000).
- `--val`: Số lượng mẫu validation (mặc định: 0 - không tạo).

### Ví dụ:

```bash
python generate_data.py --mode batch --train 10000 --test 1000 --digits 6 --format decimal
```

## 3. Chế độ SINGLE

Tạo ra một file dữ liệu duy nhất với cấu hình tùy chỉnh.

### Tham số riêng (Bắt buộc):

- `--count`: Số lượng mẫu cần tạo.
- `--strategy`: Chiến lược lấy mẫu ("balanced" hoặc "random").
- `--output`: Đường dẫn file đầu ra.

### Ví dụ:

```bash
python generate_data.py --mode single --count 500 --strategy balanced --output data/custom_data.json --digits 4
```

## 4. Chế độ EXPERIMENT (Mới)

Tự động tạo dữ liệu để chạy lại Thí nghiệm chính của bài báo:

- Chạy lặp qua các độ dài chữ số: 2, 5, 10, 15, 20, 25, 30.
- Tại mỗi độ dài, chạy 5 lần lặp (seeds) để tạo 3 tập dữ liệu mỗi lần:
  - 1 tập **Train** (1000 mẫu, Balanced).
  - 1 tập **Validation** (1000 mẫu, Balanced).
  - 1 tập **Test** (200 mẫu, Random).

Cấu trúc thư mục output:

```
data/experiment/
├── 5digits/
│   ├── train_1.json
│   ├── val_1.json
│   ├── test_1.json
│   ├── train_2.json
│   ├── val_2.json
│   ├── test_2.json
│   ├── ...
│   └── test_5.json
├── 10digits/
...
```

### Tham số riêng:

- `--base_path`: Thư mục gốc chứa dữ liệu (mặc định: `data/experiment`).
- `--seed`: Seed nền tảng để đảm bảo tính tái lập (Optional).

### Ví dụ:

```bash
python generate_data.py --mode experiment --base_path data/experiment --seed 42 --format 10e-based --only_addition
```

## ⚠️ Lưu ý quan trọng

- Tập **validation** (hay _development set_) thường được dùng để chọn checkpoint tốt nhất. Nếu dùng, nên lấy mẫu cân bằng.
- Nếu lấy mẫu **ngẫu nhiên** (random) cho số lớn, hơn 90% mẫu sẽ có số chữ số tối đa, gây ra chênh lệch phân phối.

## Định dạng (Format)

| Định dạng       | Mô tả                 | Ví dụ                     |
| --------------- | --------------------- | ------------------------- |
| decimal         | Số thập phân (cơ bản) | 123                       |
| character       | Số ký tự              | 1 2 3                     |
| fixed-character | Số ký tự cố định      | 0 1 2 3 (tối đa 4 chữ số) |
| underscore      | Số gạch dưới          | 1_2_3                     |
| words           | Cách đọc số           | one hundred twenty three  |
| 10-based        | Số 10-based           | 1 100 2 10 3              |
| 10e-based       | Số 10e-based          | 1 10e2 2 10e1 3 10e0      |

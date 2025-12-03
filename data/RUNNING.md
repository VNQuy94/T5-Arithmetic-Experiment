# 💻 CÁCH CHẠY generate_data.py 💻

## Các tham số:

- --train: Số lượng mẫu huấn luyện
- --test: Số lượng mẫu kiểm tra
- --digits: Số lượng chữ số tối đa của mẫu
- --format: Định dạng của mẫu (cần truyền đúng định dạng)
- --print: In ra một ví dụ (thêm nếu cần)

## Ví dụ lệch chạy:

```bash
py generate_data.py --train 10000 --test 1000 --digits 6 --format decimal
```

## Định dạng

| Định dạng       | Mô tả                 | Ví dụ                     |
| --------------- | --------------------- | ------------------------- |
| decimal         | Số thập phân (cơ bản) | 123                       |
| character       | Số ký tự              | 1 2 3                     |
| fixed-character | Số ký tự cố định      | 0 1 2 3 (tối đa 4 chữ số) |
| underscore      | Số gạch dưới          | 1_2_3                     |
| words           | Cách đọc số           | one hundred twenty three  |
| 10-based        | Số 10-based           | 1 100 2 10 3              |
| 10e-based       | Số 10e-based          | 1 10e2 2 10e1 3 10e0      |

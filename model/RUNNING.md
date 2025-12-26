# 💻 CÁCH CHẠY train.py 💻

## Các tham số:

# Đường dẫn
- --train_file: Đường dẫn tới file dữ liệu train
- --val_file: Đường dẫn tới file dữ liệu validation
- --test_file: Đường dẫn tới file dữ liệu test
- --output_dir: Đường dẫn output mô hình

### Note: Chạy generate_data.py để sinh ra thêm file validation, gen bên train thì là balanced, gen bên test thì là random. => Nên gen bên train (Tỉ lệ 8 - 1 - 1 cũng không tệ). Trong code của người ta là train 100000, valid 10000, test 10000. 

# Mô hình
- --model_name_or_path: Tên mô hình, bao gồm (t5-small, t5-base, t5-large)
- --max_seq_length: Độ dài của 1 chuỗi (theo token) đưa vào mô hình

## Các tham số Logging & Metadata
Các tham số này không ảnh hưởng đến quá trình train, nhưng sẽ được ghi vào file CSV kết quả để phân biệt các lần chạy.
- `--format`: Định dạng dữ liệu đang chạy (vd: `10e-based`, `decimal`, `character`).
- `--train_size_log`: Ghi chú kích thước tập train (vd: `10k`, `100k`).
- `--sampling_strategy`: Ghi chú cách lấy mẫu (vd: `balanced`, `random`).

# Huấn luyện
- --seed: Seed random
- --epochs: Số lượng epoch
- --train_batch_size: Na ná mini batch trong SGD
- --val_batch_size: Na ná mini batch trong SGD
- --lr: Hiệu chỉnh learning rate
- --num_workers: Số lượng core CPU dùng để load data
- --weight_decay: Dùng để xử lí overfitting (chatGPT không tính phí)
- --accumulate_grad_batches: Dùng để chia batch ra trường hợp batch quá to không load được.
- --check_val_every_n_epoch: Sau bao nhiêu epoch thì xét mô hình với tập validation để tạo checkpoint.

# Phần cứng (không nên đổi)
- --accelerator: Dùng gì để train (gpu, cpu, mps)
- --devices: Để 1 thôi


## Ví dụ lệnh chạy:

```bash
python .\model\train.py \
    --train_file .\data\data_train.json \
    --val_file .\data\data_val.json \
    --test_file .\data\data_test.json \
    --output_dir .\output\run_experiment_1 \
    --model_name_or_path t5-small \
    --max_seq_length 512 \
    --seed 42 \
    --epochs 50 \
    --train_batch_size 16 \
    --accumulate_grad_batches 1 \
    --check_val_every_n_epoch 1 \
    --val_batch_size 32 \
    --lr 3e-4 \
    --num_workers 2 \
    --weight_decay 0.01 \
    --accelerator gpu \
    --devices 1
```

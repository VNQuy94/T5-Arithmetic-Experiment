# 🛠️ Development Guidelines (Internal Team)

Dành cho các thành viên trong nhóm. Vui lòng đọc kỹ trước khi code.

## 1. Project Structure (Phân chia khu vực)

Code của ai người nấy quản lý, hạn chế sửa file chéo.

- **`data/`**: Chứa script sinh dữ liệu.
- **`model/`**: Chứa code train và dataset loader.

## 2. Data Interface Contract ⚠️ (QUAN TRỌNG)

Phải đảm bảo output ra file JSON đúng định dạng sau để công việc dễ dàng hơn:

```json
[
  {
    "input": "What is 3 10e1 2 10e0 plus 5 10e0?",
    "target": "3 10e1 7 10e0",
    "format": "10e-based",
    "operation": "plus",
    "length": 2
  }
]
```

## 3. Git Workflow

Không push thẳng lên `main`. Luôn tạo branch mới theo tên feature:

- `feat/data` - cho script sinh dữ liệu.
- `feat/model` - cho code liên quan đến model và training.
  Ví dụ:

```bash
git checkout -b feat/data
```

Sau khi hoàn thành, tạo pull request để review code trước khi merge vào `main`.

## 4. Environment Setup

Luôn đảm bảo cài đặt đúng thư viện trong `requirements.txt`:

```bash
pip install -r requirements.txt
```

# Investigating the Limitations of Transformers with Simple Arithmetic Tasks (Unofficial Reproduction)

This repository contains the code to reproduce the experiments presented in the paper:
**"Investigating the Limitations of Transformers with Simple Arithmetic Tasks"** (Nogueira et al., 2021).

**Objective:** To demonstrate that the surface form representation of numbers (Input Representation) is the critical factor determining whether a Transformer model (T5) can successfully learn arithmetic operations.

## 📂 Project Structure

```text
T5-Arithmetic-Experiment/
├── data/
│   ├── generate_data.py     # Script to generate arithmetic datasets
│   └── utils.py             # Helper utilities for data processing
├── model/
│   ├── train.py             # Main training script using PyTorch Lightning
│   ├── dataset.py           # Custom Dataset class
│   ├── evaluate.py          # Evaluation script
│   └── config.py            # Global configuration constants
├── experiment/              # Directory for experiment artifacts
├── requirements.txt         # Python dependencies
├── CONTRIBUTING.md          # Contributing guidelines
└── README.md                # Project documentation
```

---

## 🛠️ Setup & Installation

### 1. Environment Support

This project is optimized for:

- **Local Machines** (with NVIDIA GPU or CPU)
- **Cloud Notebooks** (Kaggle Kernels, Google Colab)

### 2. Install Dependencies

Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

_Key Libraries used:_

- **PyTorch**: Deep learning framework.
- **PyTorch Lightning**: Wrapper to organize PyTorch code and handle training loops/multi-GPU logic.
- **HuggingFace Transformers**: For the T5 model architecture and tokenizer.
- **Num2Words**: For converting numbers to text representations.

---

## ☁️ Running on Kaggle (GPU T4 x2)

To run this experiment efficiently on Kaggle, specifically leveraging the **Dual T4 GPU** setup:

### Step 1: Notebook Setup

1. Create a new Notebook in Kaggle.
2. In the right-hand panel, under **Accelerator**, select **GPU T4 x2**.

### Step 2: Running Experiments (Save Version)

Interactive mode is good for debugging, but for long training runs (which can take hours), use "Save Version".

1. **Upload Code**: You can either upload this directory as a Kaggle Dataset and copy files to `/kaggle/working/`, or pull from Git.
2. **Install Dependencies**:
   ```python
   !pip install -r requirements.txt
   ```
3. **Execute Training**:
   Add a cell to run the training script. **Crucially**, to utilize both GPUs, pass `--accelerator gpu --devices 2` (PyTorch Lightning handles distributed training automatically).

   ```python
   # Example: Train on generated data
   !python model/train.py \
       --train_file data/data_train.json \
       --val_file data/data_test.json \
       --test_file data/data_test.json \
       --output_dir outputs/run_kag_2gpu \
       --model_name_or_path t5-small \
       --format 10e-based \
       --epochs 20 \
       --train_batch_size 128 \
       --accelerator gpu \
       --devices 2
   ```

4. **Commit**: Click **Save Version** -> **Save & Run All (Commit)**. This runs the notebook in the background (up to 12 hours), allowing you to close the browser.

---

## 📊 Data Generation

The paper emphasizes **Balanced Sampling** to ensure equal distribution of digit lengths (2 to 30 digits).

**Command:**

```bash
python data/generate_data.py \
    --train 10000 \
    --test 1000 \
    --digits 30 \
    --sampling_strategy balanced \
    --format 10e-based
```

| Argument              | Description                                                     |
| :-------------------- | :-------------------------------------------------------------- |
| `--train` / `--test`  | Number of samples to generate.                                  |
| `--digits`            | Maximum number of digits (e.g., 30).                            |
| `--format`            | Input representation: `10e-based`, `decimal`, `character`, etc. |
| `--sampling_strategy` | `balanced` (recommended) or `random`.                           |

---

## 🚀 Model Training (T5 with PyTorch Lightning)

The core training logic resides in `model/train.py`. We use `T5-Small` as the baseline.

**Basic Command:**

```bash
python model/train.py \
    --train_file data/data_train.json \
    --val_file data/data_test.json \
    --test_file data/data_test.json \
    --output_dir outputs/my_experiment \
    --model_name_or_path t5-small \
    --format 10e-based \
    --max_seq_length 512 \
    --train_batch_size 128 \
    --lr 3e-4 \
    --epochs 20
```

### Key Configurations

- **Framework**: Uses `pytorch_lightning.LightningModule` to define `T5Finetuner`.
- **Max Seq Length**: The `10e-based` format is verbose. For 30-digit numbers, use `--max_seq_length 512` to avoid truncation.
- **Precision**: You can enable mixed precision for speed on GPUs using `--precision 16-mixed` (if supported by your PT Lightning version/Hardware).

---

## ⚙️ Paper Hyperparameters

To ensure fidelity to the Nogueira et al. (2021) paper:

| Hyperparameter | Value    | Flag                            |
| :------------- | :------- | :------------------------------ |
| **Model**      | T5-Small | `--model_name_or_path t5-small` |
| **Optimizer**  | AdamW    | Default                         |
| **LR**         | 3e-4     | `--lr 3e-4`                     |
| **Batch Size** | 128      | `--train_batch_size 128`        |

---

## ⚠️ Important Notes

1. **Tokenizer Parallelism Warning**: You usually can ignore `Tokenizers parallelism` warnings.

---

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Simpolette">
        <img src="https://github.com/Simpolette.png" width="100px;" alt="Simpolette"/><br />
        <sub><b>23127020 - Hoàng Minh Giang</b></sub>
      </a><br />
      T5 Model Setup
    </td>
    <td align="center">
      <a href="https://github.com/KwanTheAsian">
        <img src="https://github.com/KwanTheAsian.png" width="100px;" alt="KwanTheAsian"/><br />
        <sub><b>23127020 - Biện Xuân An</b></sub>
      </a><br />
      Model Evaluation and Documentation
    </td>
    <td align="center">
      <a href="https://github.com/PaoPao1406">
        <img src="https://github.com/PaoPao1406.png" width="100px;" alt="PaoPao1406"/><br />
        <sub><b>23127025 - Đoàn Lê Gia Bảo</b></sub>
      </a><br />
      Model Evaluation and Documentation
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/VNQuy94">
        <img src="https://github.com/VNQuy94.png" width="100px;" alt="VNQuy94"/><br />
        <sub><b>23127114 - Văn Ngọc Quý</b></sub>
      </a><br />
      Project Manager / Notebook Setup
    </td>
    <td align="center">
      <a href="https://github.com/Schooleo">
        <img src="https://github.com/Schooleo.png" width="100px;" alt="Schooleo"/><br />
        <sub><b>23127136 - Lê Nguyễn Nhật Trường</b></sub>
      </a><br />
      Dataset Generation Setup
    </td>
  </tr>
</table>

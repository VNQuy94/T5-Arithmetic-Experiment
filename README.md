# Investigating the Limitations of Transformers with Simple Arithmetic Tasks (Unofficial Reproduction)

This repository contains the code to reproduce the experiments presented in the paper:
**"Investigating the Limitations of Transformers with Simple Arithmetic Tasks"** (Nogueira et al., 2021).

**Objective:** To demonstrate that the surface form representation of numbers (Input Representation) is the critical factor determining whether a Transformer model (T5) can successfully learn arithmetic operations.

---

## 📋 Requirements

This project is optimized for environments like Google Colab or Kaggle (T4 GPU).

```bash
pip install torch torchvision torchaudio
pip install pytorch-lightning transformers datasets num2words pandas matplotlib
```

## ⚙️ Paper Configuration & Reproduction Settings

To ensure fidelity to the original paper, we use the following hyperparameters:

| Hyperparameter | Value in Paper | Configuration in this Code |
| :--- | :--- | :--- |
| **Model Architecture** | T5-Small (60M) | `--model_name_or_path t5-small` |
| **Optimizer** | AdamW | Default (HuggingFace Trainer) |
| **Learning Rate** | 0.0003 ($3 \times 10^{-4}$) | `--lr 3e-4` |
| **Batch Size** | 128 | `--train_batch_size 128`* |
| **Epochs** | 20 | `--epochs 20` |
| **Max Seq Length**| Not specified | `--max_seq_length 512` (Critical for 10e-based) |

---

## 🚀 Reproduction Instructions

### 1. Data Generation

The paper emphasizes using **Balanced Sampling** during training to ensure the model sees an equal distribution of numbers with different digit lengths (from 2 to 30 digits).

Run the following command to generate the datasets:

```bash
# Generate Balanced Training and Test data
python generate_data.py \
    --train 10000 \
    --test 1000 \
    --digits 30 \
    --sampling_strategy balanced \
    --format 10e-based
```
*Tip: Change `--format` to `decimal` or `character` for other experimental setups.*

### 2. Training Experiments (Figure 1 Reproduction)

Run the following commands to reproduce the accuracy comparison between different input representations.

#### Experiment A: 10e-based Representation (Proposed Method)
This format uses position tokens (e.g., `3 10e1 2 10e0`) and achieves the best results.

```bash
python train.py \
    --train_file data/data_train.json \
    --val_file data/data_test.json \
    --test_file data/data_test.json \
    --output_dir outputs/10e_based_run \
    --model_name_or_path t5-small \
    --format 10e-based \
    --max_seq_length 512 \
    --train_batch_size 128 \
    --lr 3e-4 \
    --epochs 20 \
    --seed 42
```

## ⚠️ Important Notes
1.  **Max Sequence Length:** The `10e-based` format significantly increases the sequence length (approx. 4x tokens per digit). You MUST set `--max_seq_length 512` (or higher) when training with numbers > 30 digits to avoid truncation, which leads to 0% accuracy.
2.  **Tokenizer Parallelism:** You may see a warning about `tokenizers parallelism`. This is normal and can be safely ignored.
```
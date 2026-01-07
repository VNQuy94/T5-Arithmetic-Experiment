# 🛠️ Contributing Guidelines

Thank you for your interest in contributing to the **T5 Arithmetic Experiment** project. Please read the following guidelines to ensure smooth collaboration.

## 1. Project Structure

Please respect the directory structure and modify files in the appropriate locations:

- **`data/`**: Scripts for data generation and processing (`generate_data.py`, `utils.py`).
- **`model/`**: Model training, evaluation logic, and dataset loading (`train.py`, `dataset.py`, `evaluate.py`).
- **`experiment/`**: Stores artifacts like model checkpoints and logs.

## 2. Data Interface Contract ⚠️ (CRITICAL)

To ensure compatibility between the data generation and training pipelines, all generated datasets must adhere to the following JSON structure:

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

Please do **not** push directly to the `main` branch. Follow this workflow:

1.  **Create a Branch**: Use descriptive names for your branches.

    - `feat/data`: For changes to data generation.
    - `feat/model`: For changes to model architecture or training loops.
    - `fix/bug-name`: For bug fixes.

    ```bash
    git checkout -b feat/your-feature-name
    ```

2.  **Commit Changes**: Write clear, concise commit messages.
3.  **Pull Request**: Open a Pull Request (PR) for review before merging into `main`.

## 4. Environment Setup

Ensure your development environment matches the project requirements:

```bash
pip install -r requirements.txt
```

---

Happy Coding! 🚀

# 🧮 Investigating Arithmetic Limitations of Transformers (T5)

> **Implementation of the paper:** *"Investigating the Limitations of Transformers with Simple Arithmetic Tasks"* (Nogueira et al., 2021).

## 1. Introduction

This project aims to reproduce the findings of Nogueira et al., demonstrating that **Surface Form Representations** (how numbers are written) significantly impact a Transformer model's ability to perform arithmetic.

We experiment with T5 models on addition tasks using different formats:
- **Decimal:** `32 + 5`
- **10E-Based:** `3 10e1 2 10e0 + 5 10e0`
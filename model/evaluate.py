import argparse
import glob
import json
import os
import csv
import pytorch_lightning as pl
import random
import torch
import config

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from torch.utils.data import DataLoader
from dataset import JSONDataset
from train import T5Finetuner, compute_exact_match

# ONLY used for Appendix G experiment, as a separate evaluation step.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate T5 on arithmetic problems.')

    # Paths
    parser.add_argument('--test_file', type=str, required=True)
    parser.add_argument('--checkpoint_path', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default='outputs')

    # Config
    parser.add_argument("--batch_size", default=config.VAL_BATCH_SIZE, type=int)
    parser.add_argument("--num_workers", default=config.NUM_WORKERS, type=int)
    parser.add_argument("--seed", default=config.SEED, type=int)
    
    # Device
    parser.add_argument("--accelerator", default="auto", type=str)
    parser.add_argument("--devices", default=1, type=int)

    args = parser.parse_args()

    pl.seed_everything(args.seed)
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Loading test data from {args.test_file}...")
    dataset_test = JSONDataset(args.test_file)
    test_dataloader = DataLoader(dataset_test, batch_size=args.batch_size,
                                 shuffle=False, num_workers=args.num_workers)

    print(f"Loading checkpoint from {args.checkpoint_path}...")
    # Load model from checkpoint
    model = T5Finetuner.load_from_checkpoint(
        args.checkpoint_path,
        map_location=lambda storage, loc: storage, # Optional safety
        train_dataloader=None,
        val_dataloader=None,
        test_dataloader=test_dataloader
    )
    
    # Override test_dataloader in the model instance
    model._test_dataloader = test_dataloader

    trainer = pl.Trainer(
        accelerator=args.accelerator,
        devices=args.devices,
        default_root_dir=args.output_dir
    )

    print("Running evaluation...")
    results = trainer.test(model, dataloaders=test_dataloader)
    
    print("Evaluation Results:", results)

    # Save results to JSON
    result_path = os.path.join(args.output_dir, "results.json")
    with open(result_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {result_path}")

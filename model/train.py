import argparse
import glob
import json
import os
import csv
import pytorch_lightning as pl
import random
import torch
import config

from pytorch_lightning.callbacks import ModelCheckpoint
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, get_cosine_schedule_with_warmup
from torch.utils.data import DataLoader

from typing import List
from dataset import JSONDataset

def compute_exact_match(predicted_answer, correct_answer) -> bool:
    predicted_answer = predicted_answer.strip().lower()
    correct_answer = correct_answer.strip().lower()
    return predicted_answer == correct_answer

class T5Finetuner(pl.LightningModule):

    def __init__(self, hparams, train_dataloader, val_dataloader, test_dataloader):
        super(T5Finetuner, self).__init__()
        
        self.save_hyperparameters(hparams)

        self.tokenizer = AutoTokenizer.from_pretrained(self.hparams.model_name_or_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.hparams.model_name_or_path)

        self._train_dataloader = train_dataloader
        self._val_dataloader = val_dataloader
        self._test_dataloader = test_dataloader

        self.test_log_data = []

    def prepare_batch(self, questions: List[str], answers: List[str]):
        input_dict = self.tokenizer.batch_encode_plus(
            list(questions), padding=True, truncation=True, 
            max_length=self.hparams.max_seq_length, return_tensors='pt'
        )

        labels = self.tokenizer.batch_encode_plus(
            list(answers), padding=True, truncation=True, 
            max_length=self.hparams.max_seq_length, return_tensors='pt'
        )['input_ids']

        input_ids = input_dict['input_ids'].to(self.model.device)
        attention_mask = input_dict['attention_mask'].to(self.model.device)
        labels = labels.to(self.model.device)

        return input_ids, attention_mask, labels

    def forward(self, **kwargs):
        return self.model(**kwargs)

    def training_step(self, batch, batch_nb):
        questions = batch['input']
        targets = batch['target']

        if batch_nb % 100 == 0:
            print(f"\n[TRAIN] Input: {questions[0]} | Target: {targets[0]}")

        input_ids, attention_mask, labels = self.prepare_batch(
            questions=questions, answers=targets)

        loss = self.model(input_ids=input_ids,
                          attention_mask=attention_mask,
                          labels=labels)[0]

        self.log('train_loss', loss, prog_bar=True, logger=True, batch_size=len(questions))
        return loss

    def inference_step(self, batch, batch_nb: int, stage: str = 'val'):
        questions = batch['input']
        correct_answers = batch['target']
        
        lengths = batch.get('length', [0] * len(questions))
        operations = batch.get('operation', ['unknown'] * len(questions))

        input_ids, attention_mask, _ = self.prepare_batch(
        questions=questions, answers=correct_answers)
        
        batch_outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            do_sample=False,
            max_length=self.hparams.max_seq_length)

        predicted_answers = [
            self.tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            for output in batch_outputs]

        exact_matches = [
            compute_exact_match(predicted_answer=predicted_answer, correct_answer=correct_answer)
            for predicted_answer, correct_answer in zip(predicted_answers, correct_answers)]

        if batch_nb % 50 == 0:
            print(f'\n[EVAL] Question: {questions[0]}')
            print(f'       Correct:  {correct_answers[0]}')
            print(f'       Predicted: {predicted_answers[0]}')
            print(f'       Exact? {exact_matches[0]}')

        if stage == 'test':
            for i in range(len(questions)):
                if hasattr(lengths[i], 'item'):
                    digit_len = lengths[i].item()
                else:
                    digit_len = lengths[i]

                log_entry = {
                    "input": questions[i],
                    "target": correct_answers[i],
                    "prediction": predicted_answers[i],
                    "is_correct": exact_matches[i],
                    "num_digits": int(digit_len),
                    "operation": operations[i],
                    "model_name": self.hparams.model_name_or_path,
                    "data_format": getattr(self.hparams, 'format', 'unknown'),
                    "train_size": getattr(self.hparams, 'train_size_log', 'unknown'),
                    "seed": self.hparams.seed
                }
                self.test_log_data.append(log_entry)

        return {'exact_matches': exact_matches}

    def validation_step(self, batch, batch_idx, stage: str = 'val'):
        metrics = self.inference_step(batch, batch_idx, stage)
        val_exact_match = sum(metrics['exact_matches']) / len(metrics['exact_matches'])
        self.log('val_exact_match', val_exact_match, prog_bar=True, on_epoch=True, batch_size=len(batch['input']))
        return metrics

    def test_step(self, batch, batch_idx, stage: str = 'test'):
        metrics = self.inference_step(batch, batch_idx, stage)
        test_exact_match = sum(metrics['exact_matches']) / len(metrics['exact_matches'])
        self.log('test_exact_match', test_exact_match, prog_bar=True, on_epoch=True, batch_size=len(batch['input']))
        return metrics
    
    def on_test_end(self):
        # Chỉ ghi file nếu có dữ liệu
        if len(self.test_log_data) > 0:
            filename = f"results_{self.hparams.model_name_or_path}_{getattr(self.hparams, 'format', 'unk')}_{getattr(self.hparams, 'train_size_log', 'unk')}sz_seed{self.hparams.seed}.csv"
            filename = filename.replace("/", "_") # Fix lỗi tên file nếu model path có dấu /
            
            save_path = os.path.join(self.hparams.output_dir, filename)
            
            keys = self.test_log_data[0].keys()
            
            # Ghi CSV
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.test_log_data)
            
            print(f"\n[INFO] Test results saved to: {save_path}")
            
            # Dọn dẹp bộ nhớ
            self.test_log_data = []

    def train_dataloader(self):
        return self._train_dataloader

    def val_dataloader(self):
        return self._val_dataloader

    def test_dataloader(self):
        return self._test_dataloader

    def configure_optimizers(self):
        no_decay = ["bias", "LayerNorm.weight"]

        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self.model.named_parameters() 
                           if not any(nd in n for nd in no_decay)],
                "weight_decay": self.hparams.weight_decay,
            },
            {
                "params": [p for n, p in self.model.named_parameters() 
                           if any(nd in n for nd in no_decay)],
                "weight_decay": 0.0,
            },
        ]

        optimizer = torch.optim.AdamW(
            optimizer_grouped_parameters, 
            lr=self.hparams.lr
        )

        total_steps = len(self._train_dataloader) * self.hparams.epochs
    
        warmup_steps = int(0.1 * total_steps)

        scheduler = get_cosine_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step",  # CRITICAL: This scheduler updates every STEP, not every epoch
                "frequency": 1
            },
        }

if __name__ == '__main__':
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    parser = argparse.ArgumentParser(description='Train T5 on arithmetic problems.')
    
    # Paths
    parser.add_argument('--train_file', type=str, required=True)
    parser.add_argument('--val_file', type=str, required=True)
    parser.add_argument('--test_file', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default='outputs')
    
    # Model
    parser.add_argument('--model_name_or_path', type=str, default='t5-small')
    parser.add_argument('--max_seq_length', type=int, default=config.MAX_LENGTH)
    
    # Training
    parser.add_argument("--seed", default=config.SEED, type=int)
    parser.add_argument("--epochs", default=config.EPOCHS, type=int)
    parser.add_argument("--train_batch_size", default=config.TRAIN_BATCH_SIZE, type=int)
    parser.add_argument("--val_batch_size", default=config.VAL_BATCH_SIZE, type=int)
    parser.add_argument("--lr", default=config.LEARNING_RATE, type=float)
    parser.add_argument("--num_workers", default=config.NUM_WORKERS, type=int)
    

    parser.add_argument("--format", type=str, default="unknown", help="Format used: 10e-based, decimal...")
    parser.add_argument("--train_size_log", type=str, default="unknown", help="Size of training set (e.g., 10k)")
    parser.add_argument("--sampling_strategy", type=str, default="unknown", help="balanced or random")
    
    parser.add_argument("--weight_decay", default=config.WEIGHT_DECAY, type=float, help="Weight decay if we apply some.")

    # Hardware
    parser.add_argument("--accelerator", default="auto", type=str, help="cpu, gpu, mps")
    parser.add_argument("--devices", default=1, help="number of devices")

    args = parser.parse_args()

    print('Training Arguments:', args)

    os.makedirs(args.output_dir, exist_ok=True)

    random.seed(args.seed)
    pl.seed_everything(args.seed)

    # --- Load Datasets ---
    print(f"Loading train data from {args.train_file}...")
    dataset_train = JSONDataset(args.train_file)
    
    print(f"Loading validation data from {args.val_file}...")
    dataset_val = JSONDataset(args.val_file)
    
    print(f"Loading test data from {args.test_file}...")
    dataset_test = JSONDataset(args.test_file)

    train_dataloader = DataLoader(dataset_train, batch_size=args.train_batch_size,
                                  shuffle=True, num_workers=args.num_workers)

    val_dataloader = DataLoader(dataset_val, batch_size=args.val_batch_size, shuffle=False,
                                num_workers=args.num_workers)

    test_dataloader = DataLoader(dataset_test, batch_size=args.val_batch_size,
                                 shuffle=False, num_workers=args.num_workers)

    # --- Setup Trainer ---
    checkpoint_callback = ModelCheckpoint(
        dirpath=args.output_dir,
        filename='{epoch}-{val_exact_match:.4f}',
        verbose=True, 
        save_last=False, 
        save_top_k=1, 
        mode='max', 
        monitor='val_exact_match',
        save_weights_only=False
    )

    trainer = pl.Trainer(
        accelerator=args.accelerator,
        devices=args.devices,
        max_epochs=args.epochs,
        callbacks=[checkpoint_callback],
        default_root_dir=args.output_dir
    )

    # --- Init Model ---
    model = T5Finetuner(hparams=args,
                        train_dataloader=train_dataloader,
                        val_dataloader=val_dataloader,
                        test_dataloader=test_dataloader)

    # --- Train ---
    trainer.fit(model)

    # --- Test ---
    # Load best checkpoint
    checkpoint_path = checkpoint_callback.best_model_path
    if checkpoint_path:
        print(f"Loading best checkpoint: {checkpoint_path}")
        model = T5Finetuner.load_from_checkpoint(checkpoint_path,
                                                hparams=args,
                                                train_dataloader=train_dataloader,
                                                val_dataloader=val_dataloader,
                                                test_dataloader=test_dataloader)

    results = trainer.test(model)

    # Save results
    output_results = {
        'seed': args.seed,
        'test_exact_match': results[0]['test_exact_match']
    }

    with open(os.path.join(args.output_dir, 'results.json'), 'w') as fout:
        json.dump(output_results, fout, indent=2)

    print('Done!')
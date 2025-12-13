import json
from torch.utils.data import Dataset

class JSONDataset(Dataset):
    def __init__(self, file_path):
        """
        Args:
            file_path (str): Path to the json file (e.g., 'data/data_train.json')
        """
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        
        return {
            "input": item['input'],
            "target": item['target'],
            "length": item.get('length', 0),        
            "operation": item.get('operation', 'unknown') 
        } 
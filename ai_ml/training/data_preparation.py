"""
CivicResolve - Data Preparation
"""

import os
import shutil
import yaml
import random
import sys
from pathlib import Path

# Fix import path to allow running as module
# We need to add 'CivicResolve' (root) to sys.path
current_file = Path(__file__).resolve()
project_root = current_file.parents[2] # Go up: training -> ai_ml -> CivicResolve
sys.path.append(str(project_root))

from ai_ml.utils.logger import setup_logger

class CivicDatasetFilter:
    def __init__(self):
        # Initialize Logger
        self.logger = setup_logger("data_preparation")
        
        # ROBUST PATH CALCULATION
        # This ensures we always find the root 'CivicResolve' folder
        # relative to where this script file is located.
        self.project_root = Path(__file__).resolve().parents[2]
        
        # Paths
        self.paths = {
            # Input: Scans this folder and ALL subfolders
            'raw_source': self.project_root / "data" / "archive",
            # Output: Clean YOLO structure
            'yolo_data': self.project_root / "data" / "yolo_format"
        }
        
        # Target IDs (From your 10-class list)
        self.target_class_ids = [1, 5] 
        self.new_class_mapping = {1: 0, 5: 1}
        
        self.logger.info(f"Project Root detected as: {self.project_root}")
        self.logger.info(f"Looking for data in: {self.paths['raw_source']}")

    def setup_output_directories(self):
        """Create clean output directories."""
        if self.paths['yolo_data'].exists():
            shutil.rmtree(self.paths['yolo_data'])
            
        for split in ['train', 'val']:
            (self.paths['yolo_data'] / "images" / split).mkdir(parents=True, exist_ok=True)
            (self.paths['yolo_data'] / "labels" / split).mkdir(parents=True, exist_ok=True)
            
        self.logger.info(f"Created output directory: {self.paths['yolo_data']}")

    def process_data(self):
        """Recursively find all images, filter them, and split into train/val."""
        
        # 1. DEBUG: Verify source directory exists
        if not self.paths['raw_source'].exists():
            self.logger.error(f"Source folder not found: {self.paths['raw_source']}")
            self.logger.info("Listing contents of 'data' folder to help debug:")
            data_dir = self.project_root / "data"
            if data_dir.exists():
                for item in data_dir.iterdir():
                    self.logger.info(f" - {item.name}")
            return

        self.logger.info("Scanning for images recursively...")
        
        # 2. Find ALL images
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        all_images = []
        for ext in extensions:
            all_images.extend(list(self.paths['raw_source'].rglob(ext)))
            all_images.extend(list(self.paths['raw_source'].rglob(ext.upper())))
            
        if not all_images:
            self.logger.error(f"No images found in {self.paths['raw_source']}")
            return

        self.logger.info(f"Found {len(all_images)} total images. Checking labels...")
        
        # 3. Process Images
        valid_samples = []
        for img_path in all_images:
            # Check for label file
            label_path = img_path.with_suffix('.txt')
            
            # Alternative: Check parallel 'labels' folder
            if not label_path.exists():
                potential_path = str(label_path).replace('images', 'labels')
                if os.path.exists(potential_path):
                    label_path = Path(potential_path)

            if not label_path.exists():
                continue

            # Check content
            new_content = self._filter_label_file(label_path)
            
            if new_content:
                valid_samples.append({
                    'img_path': img_path,
                    'label_content': new_content
                })

        self.logger.info(f"Found {len(valid_samples)} valid samples (Potholes/Garbage).")
        
        if len(valid_samples) == 0:
            self.logger.warning("Images found, but no labels matched IDs 1 or 5.")
            return

        # 4. Shuffle and Split
        random.shuffle(valid_samples)
        split_idx = int(len(valid_samples) * 0.8)
        
        train_samples = valid_samples[:split_idx]
        val_samples = valid_samples[split_idx:]
        
        self._save_split(train_samples, 'train')
        self._save_split(val_samples, 'val')
        self._create_yaml()

    def _filter_label_file(self, label_path):
        try:
            with open(label_path, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                
                try:
                    class_id = int(parts[0])
                except ValueError:
                    continue 
                
                if class_id in self.target_class_ids:
                    new_id = self.new_class_mapping[class_id]
                    new_lines.append(f"{new_id} {' '.join(parts[1:])}")
            
            return "\n".join(new_lines) if new_lines else None
            
        except Exception as e:
            self.logger.error(f"Error reading {label_path}: {e}")
            return None

    def _save_split(self, samples, split_name):
        self.logger.info(f"Saving {len(samples)} samples to {split_name}...")
        
        dst_img_dir = self.paths['yolo_data'] / "images" / split_name
        dst_lbl_dir = self.paths['yolo_data'] / "labels" / split_name
        
        for i, sample in enumerate(samples):
            ext = sample['img_path'].suffix
            new_filename = f"{split_name}_{i:05d}"
            
            try:
                shutil.copy(sample['img_path'], dst_img_dir / f"{new_filename}{ext}")
                with open(dst_lbl_dir / f"{new_filename}.txt", 'w') as f:
                    f.write(sample['label_content'])
            except Exception as e:
                self.logger.error(f"Failed to copy {sample['img_path'].name}: {e}")

    def _create_yaml(self):
        config = {
            'path': str(self.paths['yolo_data'].absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'nc': 2,
            'names': ['pothole', 'garbage']
        }
        
        yaml_path = self.paths['yolo_data'] / 'dataset.yaml'
        with open(yaml_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
        self.logger.info(f"Config created at {yaml_path}")

def main():
    processor = CivicDatasetFilter()
    processor.setup_output_directories()
    processor.process_data()

if __name__ == "__main__":
    main()
import shutil
import sys
import torch
from pathlib import Path
from ultralytics import YOLO

# Robust Path Setup: ai_ml/training/train_model.py -> CivicResolve
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from ai_ml.utils.logger import setup_logger

class CivicModelTrainer:
    def __init__(self):
        self.logger = setup_logger("model_trainer")
        self.root = project_root
        
        self.paths = {
            'dataset': self.root / "data" / "yolo_format" / "dataset.yaml",
            'models': self.root / "ai_ml" / "models",
            'runs': self.root / "ai_ml" / "runs"
        }
        
        self.paths['models'].mkdir(parents=True, exist_ok=True)
        self.device = '0' if torch.cuda.is_available() else 'cpu'

    def train(self, epochs=50, imgsz=416, batch=8):
        if not self.paths['dataset'].exists():
            self.logger.error(f"Dataset config missing: {self.paths['dataset']}")
            return

        self.logger.info(f"Starting Training on {self.device}...")
        self.logger.info(f"Image size: {imgsz}, Batch size: {batch}")
        
        try:
            # Load nano model (fastest)
            model = YOLO('yolov8n.pt') 
            
            # Train
            results = model.train(
                data=str(self.paths['dataset']),
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                device=self.device,
                project=str(self.paths['runs']),
                name='civic_resolve',
                exist_ok=True,
                verbose=True
            )
            
            # Save final best model to main models dir
            best_weight = Path(results.save_dir) / "weights" / "best.pt"
            target_path = self.paths['models'] / "best_civic_model.pt"
            
            if best_weight.exists():
                shutil.copy(best_weight, target_path)
                self.logger.info(f"✅ Success. Model saved: {target_path}")
            
        except Exception as e:
            self.logger.error(f"Training failed: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=416, help="Image size for training")
    parser.add_argument("--batch", type=int, default=8, help="Batch size")
    args = parser.parse_args()

    trainer = CivicModelTrainer()
    trainer.train(epochs=args.epochs, imgsz=args.imgsz, batch=args.batch)
import cv2
import sys
import argparse
from pathlib import Path
from ultralytics import YOLO

# Robust Path Setup: tests/test_model.py -> CivicResolve
# We go up 1 level to reach the project root
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from ai_ml.utils.logger import setup_logger

class CivicModelTester:
    def __init__(self):
        self.logger = setup_logger("model_tester")
        self.root = project_root
        
        # Path to best model (saved by train_model.py)
        self.model_path = self.root / "ai_ml" / "models" / "best_civic_model.pt"
        
        if not self.model_path.exists():
            self.logger.error(f"Model not found: {self.model_path}")
            self.logger.info("Please run ai_ml/training/train_model.py first.")
            sys.exit(1)
            
        self.logger.info(f"Loading model: {self.model_path}")
        self.model = YOLO(str(self.model_path))

    def test_image(self, image_path):
        """Run inference on a single image."""
        img_path = Path(image_path)
        if not img_path.exists():
            self.logger.error(f"Image not found: {img_path}")
            return

        self.logger.info(f"Testing on: {img_path}")
        
        # Run Inference
        results = self.model(img_path, conf=0.25)
        
        # Log detections
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = self.model.names[cls_id]
                self.logger.info(f"Found {name} ({conf:.1%})")

        # Display Result
        results[0].show() 

    def test_webcam(self):
        """Run real-time inference on webcam."""
        self.logger.info("Starting Webcam. Press 'q' to exit.")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.logger.error("Could not open webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret: break

            # Inference
            results = self.model(frame, conf=0.4, verbose=False)
            
            # Plot annotations on frame
            annotated_frame = results[0].plot()

            cv2.imshow("CivicResolve - Live", annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", type=str, help="Path to image file")
    parser.add_argument("--webcam", action="store_true", help="Run webcam test")
    args = parser.parse_args()

    tester = CivicModelTester()

    if args.img:
        tester.test_image(args.img)
    elif args.webcam:
        tester.test_webcam()
    else:
        print("Usage: python tests/test_model.py --webcam OR --img <path_to_image>")
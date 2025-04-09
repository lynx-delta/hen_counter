
from ultralytics import YOLO


def train_model(data_path, project_path):

    # Load a pretrained model
    model = YOLO('yolo11s.pt')

    # Train the model (transfer learning)
    model.train(
        data=data_path,
        epochs=100,
        patience=20,
        imgsz=640,
        batch=8,
        project=project_path,
        name='yolo11_640_480_x',
        device='cpu',
        optimizer='auto',
        seed=42,
        dropout=0.05 ,
        plots=True
        )


data_path = '/home/ubuntu/Model/hens_data.yaml'
project_path = '/home/ubuntu/Model/training_runs/'


if __name__ == '__main__':
    train_model(data_path, project_path)
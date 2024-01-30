import os
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from train_model import Net  # Import your model class here



device = "cuda"

def load_model(model_path):
    model = Net()  # Initialize your model
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def evaluate_model(model, test_loader):
    y_true, y_pred = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(predicted.cpu().numpy())

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    return accuracy, precision, recall, f1

def main():
    model_dir = 'SavedModels'  # Directory where models are saved
    test_transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        # Add other transformations as per your requirement
    ])

    test_dataset = datasets.ImageFolder(root='../Augmented_Images', transform=test_transform)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=True, num_workers=4)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    metrics = {'accuracy': [], 'precision': [], 'recall': [], 'f1': []}
    model_epochs = []

    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]
    model_files.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))

    for filename in model_files:
        epoch = int(filename.split('_')[2].split('.')[0])
        model_epochs.append(epoch)
        model_path = os.path.join(model_dir, filename)
        model = load_model(model_path)
        model.to(device)

        accuracy, precision, recall, f1 = evaluate_model(model, test_loader)
        metrics['accuracy'].append(accuracy)
        metrics['precision'].append(precision)
        metrics['recall'].append(recall)
        metrics['f1'].append(f1)

        # Print metrics for the current model
        print(f"Epoch {epoch}: Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, "
                f"Recall: {recall:.2f}, F1 Score: {f1:.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(model_epochs, metrics['accuracy'], label='Accuracy')
    plt.plot(model_epochs, metrics['precision'], label='Precision')
    plt.plot(model_epochs, metrics['recall'], label='Recall')
    plt.plot(model_epochs, metrics['f1'], label='F1 Score')
    plt.xlabel('Epochs')
    plt.ylabel('Metrics')
    plt.title('Model Performance over Epochs')
    plt.legend()
    plt.savefig('model_performance.png')
    plt.show()

if __name__ == '__main__':
    main()

import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter
import torch.nn.functional as F
from tqdm import tqdm


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 6, 5)
        self.pool_layer = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(6, 16, 5) 
        self.fc1 = torch.nn.Linear(16 * 61 * 61, 120)# 5x5 from image dimension
        self.fc2 = torch.nn.Linear(120, 84)
        self.fc3 = torch.nn.Linear(84, 3)

    def forward(self, x):
        x = self.pool_layer(F.relu(self.conv1(x)))
        x = self.pool_layer(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 61 * 61)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def imshow(img):
  npimg = img.numpy() # convert to numpy objects
  plt.imshow(np.transpose(npimg, (1, 2, 0)))
  plt.show()

def calculate_accuracy(loader, net):
        correct = 0
        total = 0
        with torch.no_grad():
            for data in loader:
                images, labels = data[0].to("cuda"), data[1].to("cuda")
                outputs = net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        return 100 * correct / total

batch_size = 32

model_save_path = 'SavedModels'  # Define the directory name

def main():
    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)


    print('Using device:', torch.cuda.get_device_name(0))

    classes = ("Benign_Pics", "Malignant_Pics", "Normal_Pics")


    transform = transforms.Compose([
        torchvision.transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),          # Convert images to PyTorch tensors
    ])

    dataset = torchvision.datasets.ImageFolder(root='../Augmented_Images', transform=transform)

    n = len(dataset)  # total number of examples
    n_test = int(0.2 * n)  # take ~20% for test

    train_set, test_set = torch.utils.data.random_split(dataset, [int(len(dataset)*.8), len(dataset)-int(len(dataset)*.8)])


    train_classes = [dataset.targets[i] for i in train_set.indices]
    print(Counter(train_classes)) # if doesn' work: Counter(i.item() for i in train_classes)

    test_classes = [dataset.targets[i] for i in test_set.indices]
    print(Counter(test_classes)) # if doesn' work: Counter(i.item() for i in train_classes)


    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=True)







        
    net = Net()
    print(net)

    net.to("cuda")

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr = 0.001, momentum=0.9)

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record()

    

    epoch_losses = []
    test_accuracies = []
    train_accuracies = []

    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

    for epoch in tqdm(range(100), desc='Epochs'):
        total_running_loss = 0.0
        running_loss = 0.0
        count = 0
        for i, data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data[0].to('cuda'), data[1].to('cuda')  # Move data to GPU

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            total_running_loss += loss.item()
            if i % 100 == 99:    # print every 100 mini-batches
                print('[%d, %5d] loss: %.3f' %
                    (epoch + 1, i + 1, running_loss / 100))
                
                epoch_losses.append(running_loss / 100)
                running_loss = 0.0
            count+=1
        
        scheduler.step()

        print(f'Epoch {epoch+1}, Loss: {total_running_loss/count:.3f}')
        if epoch % 5 == 4:
            model_filename = f'net_epoch_{epoch+1}.pth'
            torch.save(net.state_dict(), os.path.join(model_save_path, model_filename))

            print(f'Model saved as {model_filename}')
        test_accuracy = calculate_accuracy(test_loader, net)
        test_accuracies.append(test_accuracy)
        print(f'Epoch {epoch+1}, Test accuracy: {test_accuracy}%')
        train_accuracy = calculate_accuracy(train_loader, net)
        print(f'Epoch {epoch+1}, Train accuracy: {train_accuracy}%')
        train_accuracies.append(train_accuracy)

    end.record()

    torch.cuda.synchronize()

    print('Finished Training')
    print(start.elapsed_time(end))  # milliseconds


    plt.figure(figsize=(12, 6))

    # Plotting loss
    plt.subplot(1, 2, 1)
    plt.plot(epoch_losses, label='Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plotting accuracies
    plt.subplot(1, 2, 2)
    plt.plot(test_accuracies, label='Test Accuracy')
    plt.plot(train_accuracies, label='Train Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()


    test_accuracy = calculate_accuracy(test_loader, net)
    print(f'Final Test accuracy: {test_accuracy}%')

if __name__ == '__main__':
    main()
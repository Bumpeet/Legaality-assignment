from metrics import accuracy
from model import ContrastiveLoss, SigNet
from dataloaders import get_data_loader
import os
from PIL import ImageOps
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms

seed = 2020
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print('Device: {}'.format(device))

def train(model, optimizer, criterion, dataloader, log_interval=50):
    model.train()
    running_loss = 0
    number_samples = 0

    for batch_idx, (x1, x2, y) in enumerate(dataloader):
        x1, x2, y = x1.to(device), x2.to(device), y.to(device)

        optimizer.zero_grad()
        x1, x2 = model(x1, x2)
        loss = criterion(x1, x2, y)
        loss.backward()
        optimizer.step()

        number_samples += len(x1)
        running_loss += loss.item() * len(x1)
        if (batch_idx + 1) % log_interval == 0 or batch_idx == len(dataloader) - 1:
            print('{}/{}: Loss: {:.4f}'.format(batch_idx+1, len(dataloader), running_loss / number_samples))
            running_loss = 0
            number_samples = 0

@torch.no_grad()
def eval(model, criterion, dataloader, log_interval=50):
    model.eval()
    running_loss = 0
    number_samples = 0

    distances = []

    for batch_idx, (x1, x2, y) in enumerate(dataloader):
        x1, x2, y = x1.to(device), x2.to(device), y.to(device)

        x1, x2 = model(x1, x2)
        loss = criterion(x1, x2, y)
        distances.extend(zip(torch.pairwise_distance(x1, x2, 2).cpu().tolist(), y.cpu().tolist()))

        number_samples += len(x1)
        running_loss += loss.item() * len(x1)

        if (batch_idx + 1) % log_interval == 0 or batch_idx == len(dataloader) - 1:
            print('{}/{}: Loss: {:.4f}'.format(batch_idx+1, len(dataloader), running_loss / number_samples))

    distances, y = zip(*distances)
    distances, y = torch.tensor(distances), torch.tensor(y)
    max_accuracy = accuracy(distances, y)
    print(f'Max accuracy: {max_accuracy}')
    return running_loss / number_samples, max_accuracy


if __name__=='__main__':
    class arguments():
        batch_size = 16
        lr = 1e-5
        dataset = 'cedar'

    args = arguments()


    model = SigNet().to(device)
    criterion = ContrastiveLoss(alpha=1, beta=1, margin=1).to(device)
    # optimizer = optim.RMSprop(model.parameters(), lr=1e-5, eps=1e-8, weight_decay=5e-4, momentum=0.9)
    optimizer_adam = optim.Adam(model.parameters(), 1e-5, (0.9,0.999))
    scheduler = optim.lr_scheduler.StepLR(optimizer_adam, 5, 0.1)
    num_epochs = 20

    image_transform = transforms.Compose([
        transforms.Resize((155, 220)),
        ImageOps.invert,
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    trainloader = get_data_loader(is_train=True, batch_size=args.batch_size, image_transform=image_transform, dataset=args.dataset)
    testloader = get_data_loader(is_train=False, batch_size=args.batch_size, image_transform=image_transform, dataset=args.dataset)
    os.makedirs('checkpoints', exist_ok=True)

    model.train()
    print(model)
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs))
        print('Training', '-'*20)
        train(model, optimizer_adam, criterion, trainloader)
        print('Evaluating', '-'*20)
        loss, acc = eval(model, criterion, testloader)
        scheduler.step()

        to_save = {
            'model': model.state_dict(),
            'scheduler': scheduler.state_dict(),
            'optim': optimizer_adam.state_dict(),
        }

        print('Saving checkpoint..')
        torch.save(to_save, 'checkpoints/epoch_{}_loss_{:.3f}_acc_{:.3f}.pt'.format(epoch, loss, acc))

    print('Done')
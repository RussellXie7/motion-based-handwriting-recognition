#cell 0
import torch
import data_loader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#cell 1
torch.cuda.is_available()

#cell 2
trainx, devx, testx, trainy, devy, testy = data_loader.load_all_classic_random_split(flatten=False)

#cell 3
trainx, trainy = data_loader.augment_train_set(trainx, trainy, augment_prop=3, is_flattened=False)
trainx.shape, devx.shape, testx.shape, trainy.shape, devy.shape, testy.shape

#cell 4
BATCH_SIZE = 500

def get_dataloader(x, y, batch_size):
    dataset = [(x[i].T, y[i]) for i in range(y.shape[0])]
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

trainloader = get_dataloader(trainx, trainy, BATCH_SIZE)
devloader = get_dataloader(devx, devy, BATCH_SIZE)
testloader = get_dataloader(testx, testy, BATCH_SIZE)

#cell 5
_, num_feature, num_channel = trainx.shape
num_feature, num_channel

#cell 6
def acc(data_loader):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in data_loader:
            x, y = data
            if torch.cuda.is_available():
                x = x.cuda()
                y = y.cuda()
                
            outputs = net(x.float())
            _, predicted = torch.max(outputs.data, 1)
            
            w = torch.sum((predicted - y) != 0).item()
            r = len(y) - w
            correct += r 
            total += len(y)
    return correct / total

#cell 7
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv1d(
            in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1
        )  
        # 16 channel, num_feature
        self.pool1 = nn.MaxPool1d(kernel_size=3, stride=1, padding=1)
        # 16 channel, num_feature

        self.conv2 = nn.Conv1d(
            in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2
        )
        # 32 channel, num_feature
        self.pool2 = nn.MaxPool1d(kernel_size=5, stride=1, padding=2)
        # 32 channel, num_feature
        
        self.conv3 = nn.Conv1d(
            in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2
        )
        self.pool3 = nn.MaxPool1d(kernel_size=5, stride=1, padding=2)

        self.fc1 = nn.Linear(num_feature * 64, 3200)
        self.dropout = nn.Dropout(p=0.2)
        self.fc2 = nn.Linear(3200, 1600)
        self.fc3 = nn.Linear(1600, 500)
        self.fc4 = nn.Linear(500, 26)

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(-1, num_feature * 64)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x
net = Net()
if torch.cuda.is_available():
    net.cuda()
net

#cell 8
criterion = nn.CrossEntropyLoss()
# optimizer = optim.SGD(net.parameters(), lr=0.00001, momentum=0.9)
optimizer = optim.Adam(net.parameters(), lr=0.0001)

for epoch in range(20):  # loop over the dataset multiple times
    running_loss = 0.0
    for i, data in enumerate(trainloader):
        print(f'{i if i%20==0 else ""}.', end='')

        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data
        if torch.cuda.is_available():
            inputs = inputs.cuda()
            labels = labels.cuda()

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        
        outputs = net(inputs.float())
        loss = criterion(outputs, labels.long())
        loss.backward()
        optimizer.step()

    trainacc = acc(trainloader)
    devacc = acc(devloader)

    print('')
    print(f'Epoch {epoch} trainacc={trainacc} devacc={devacc}')

print('Finished Training')

#cell 9
acc(testloader)

#cell 10


#cell 11


#cell 12


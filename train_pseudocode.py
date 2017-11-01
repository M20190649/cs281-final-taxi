import torch
from torch import nn
from network import *


W = nn.Embedding(...)
network = Network()

def predict(trip):
    start = trip['start']
    end = trip['end']
    n1, n2 = network.get_node(start), network.get_node(end)
    path = network.get_path(n1, n2)
    t = W(path).sum()
    return t

def loss_fn(trip):
    return (trip['time'] - predict(trip)).pow(2)

optimizer = torch.optim.SGD([W], ...)

num_epoch = 100
with tqdm(total=num_epoch * len(train_iter)) as pbar:
    for epoch in range(num_epoch):
        total_loss = 0
        for trip in train_iter:
            pbar.update(1)
            loss = loss_fn(trip)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.data[0]
        print('Epoch', epoch, 'Loss', total_loss / len(train_iter))




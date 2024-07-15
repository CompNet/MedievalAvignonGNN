import torch
from tqdm import tqdm
from torch_geometric.utils import from_networkx
from graph_generator import *
# from models.GCN import GCN
from torch_geometric.nn.models import GCN


if __name__ == '__main__':
    # Données
    graphs = load(15866802)  # petites positions (0, 1)
    # graphs = load(15948057)  # grandes positions (-100, 100)
    data = from_networkx(graphs[0])

    data.x = torch.zeros(data.y.shape[0], 10)
    torch.nn.init.uniform_(data.x)
    train_mask = [False if bool(np.isnan(i[0])) else True for i in data.pos]  # based on degraded graph
    test_mask = [not i for i in train_mask]

    # Modèle
    # model = GCN(input_dim=10, hidden_dim=16, output_dim=2)
    model = GCN(in_channels=-1, hidden_channels=16, out_channels=2, num_layers=2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    lossfn = torch.nn.MSELoss()

    # Entraînement
    epochs = 1000  # sur-entraînement ? sous-entraînement ?
    model.train()  # set train flag
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = lossfn(out[train_mask], data.y[train_mask])
        loss.backward()
        optimizer.step()

        if epoch % 50 == 0:
            print(f'Epoch:{epoch+1}: loss is {loss:.4f}')

    # Test
    model.eval()  # set test flag
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        loss = lossfn(out[test_mask], data.y[test_mask])
        print('test loss: ', loss)
        print('out ', out)
        print('verité terrain', data.y)
        final = data.pos.clone()
        final[test_mask] = out[test_mask]
        print('FINAL: ', final)

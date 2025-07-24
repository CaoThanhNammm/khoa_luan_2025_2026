# Đây là class dùng để load tập dữ liệu của mag và prime để truy xuất tạo ra KB và VDB
from ogb.nodeproppred import NodePropPredDataset

d_name = 'ogbn-prime'
dataset = NodePropPredDataset(name = d_name)

print(dataset)
# split_idx = dataset.get_idx_split()
# train_idx, valid_idx, test_idx = split_idx["train"], split_idx["valid"], split_idx["test"]
# graph = dataset[0]

























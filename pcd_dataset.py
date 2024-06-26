import torch
from torch.utils.data import Dataset, DataLoader
import os
import open3d as o3d
from pathlib import Path


class PointCloudDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.samples = []

        # Iterate through all subdirectories in the root_dir/output
        for num_points_dir in self.root_dir.glob("output/*"):
            if num_points_dir.is_dir():
                num_points = int(num_points_dir.name)  # Get the number of points
                for ply_file in num_points_dir.glob("*.ply"):
                    self.samples.append((ply_file, num_points))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        ply_file, label = self.samples[idx]
        points = self.read_point_cloud(str(ply_file))  # Read point cloud from PLY file
        return points, label

    def read_point_cloud(self, ply_file):
        pcd = o3d.io.read_point_cloud(ply_file)
        points = torch.tensor(pcd.points).float()  # Convert to torch tensor
        return points


# Example usage:
if __name__ == "__main__":
    dataset_path = "dataset"
    dataset = PointCloudDataset(dataset_path)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # Iterate over the dataloader
    for i, (points, label) in enumerate(dataloader):
        print(f"Sample {i+1}: Points shape = {points.shape}, Label = {label}")

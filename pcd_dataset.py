from pathlib import Path
import torch
from torch.utils.data import Dataset, DataLoader
import open3d as o3d


class PointCloudDataset(Dataset):
    def __init__(self, data_folder: str, point_numbers: int):
        """
        Args:
            data_folder (str): Path to the folder containing PLY files organized by the number of points.
            point_numbers (list): List of point numbers used for subfolders.
        """
        self.data_folder = Path(data_folder) / "ply"
        self.point_numbers = point_numbers
        self.files = []
        self.labels = []

        subfolder = self.data_folder / str(point_numbers)
        for file in subfolder.iterdir():
            if file.is_file() and file.suffix == ".ply":
                self.files.append(file)
                self.labels.append(file.stem)
                print(f"Loaded file: {file} with label: {file.stem}")
            else:
                print(f"File is not a file or not a ply file ! : {file}")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        file_path = self.files[idx]
        label = self.labels[idx]

        try:
            # Load the point cloud
            pcd = o3d.io.read_point_cloud(str(file_path))
            points = torch.tensor(pcd.points, dtype=torch.float32)
            return points, label
        except Exception as e:
            print(f"Error loading point cloud from {file_path}: {e}")
            return None, None


def collate_fn(batch):
    """Custom collate function to handle batches of point clouds and labels"""
    points, labels = zip(*batch)
    # Filter out any None values that resulted from loading errors
    points = [p for p in points if p is not None]
    labels = [l for l in labels if l is not None]
    points = torch.stack(points)
    labels = torch.tensor(labels, dtype=torch.long)
    return points, labels


def create_dataloader(
    data_folder: str, point_numbers: int, batch_size: int, shuffle: bool = True
):
    dataset = PointCloudDataset(data_folder, point_numbers)
    dataloader = DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle, collate_fn=collate_fn
    )
    return dataloader


if __name__ == "__main__":
    data_folder = "dataset_step/data/ply"
    point_numbers = 1000
    batch_size = 4

    dataloader = create_dataloader(data_folder, point_numbers, batch_size)

    # Iterate through the DataLoader
    for batch_idx, (points, labels) in enumerate(dataloader):
        print(f"Batch {batch_idx + 1}")
        print(f"Points: {points.size()}")  # (batch_size, num_points, 3)
        print(f"Labels: {labels}")

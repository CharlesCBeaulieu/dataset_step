from pathlib import Path
import open3d
import trimesh


def convert_to_stl(input_folder: str, stl_folder: str):
    """
    Convert STEP files in the input folder to STL format and save them in the STL folder.

    Args:
        input_folder (str): Path to the folder containing the STEP files.
        stl_folder (str): Path to the folder where the converted STL files will be saved.
    """
    input_folder = Path(input_folder)
    stl_folder = Path(stl_folder)
    stl_folder.mkdir(parents=True, exist_ok=True)

    for file in input_folder.iterdir():
        if (
            file.is_file()
            and file.suffix.lower() == ".stp"
            and not file.name.startswith("._")
        ):
            try:
                # Load the STEP file and convert to STL
                mesh = trimesh.Trimesh(
                    **trimesh.interfaces.gmsh.load_gmsh(
                        file_name=str(file), gmsh_args=[("Mesh.Algorithm", 5)]
                    )
                )
                mesh.export(str(stl_folder / (file.stem + ".stl")))
            except Exception as e:
                print(f"Error processing file {file}: {e}")


def generate_ply_folders(stl_folder: str, ply_folder: str, number_of_points: list):
    """
    Generate PLY folders by sampling points from STL files.

    Args:
        stl_folder (str): The path to the folder containing STL files.
        ply_folder (str): The path to the folder where the PLY folders will be generated.
        number_of_points (list): A list of integers representing the number of points to sample.

    Returns:
        None
    """
    stl_folder = Path(stl_folder)
    ply_folder = Path(ply_folder)
    ply_folder.mkdir(parents=True, exist_ok=True)

    # Process the STL files
    for num_points in number_of_points:
        # Create subfolder for the current number of points
        subfolder = ply_folder / str(num_points)
        subfolder.mkdir(parents=True, exist_ok=True)

        for file in stl_folder.iterdir():
            if (
                file.is_file()
                and file.suffix.lower() == ".stl"
                and not file.name.startswith("._")
            ):
                try:
                    # Read STL and sample points
                    pcd = open3d.io.read_triangle_mesh(str(file))
                    sampled_pcd = pcd.sample_points_poisson_disk(num_points)

                    # Save the sampled point cloud to a PLY file in the appropriate subfolder
                    ply_output_file = subfolder / (file.stem + f"_{num_points}.ply")
                    open3d.io.write_point_cloud(str(ply_output_file), sampled_pcd)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")


def generate_dataset_from_step(
    dataset_path: str, number_of_points: list = [1000, 5000, 10000]
):
    """
    Generate dataset from a given step.

    Args:
        dataset_path (str): The path to the dataset.
        number_of_points (list, optional): A list of integers representing the number of points to generate for each step. Defaults to [1000, 5000, 10000].

    Returns:
        None
    """
    input_folder = Path(dataset_path)
    output_folder = input_folder.parent
    stl_folder = output_folder / "stl"
    ply_folder = output_folder / "ply"

    # Convert STEP files to STL
    convert_to_stl(input_folder, stl_folder)

    # Generate PLY folders
    generate_ply_folders(stl_folder, ply_folder, number_of_points)


if __name__ == "__main__":
    dataset_path = "dataset_step/data/STEP_test"
    generate_dataset_from_step(dataset_path, [1000, 5000, 10000])

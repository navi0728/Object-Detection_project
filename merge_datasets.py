import os
import shutil
from tqdm import tqdm  # Import tqdm for the progress bar

def merge_directories(src_dir1, src_dir2, dest_dir):
    # Check if destination directory exists, create if not
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Define subdirectories that should exist in the destination directory
    subdirectories = ['train', 'test', 'validation']

    # Function to copy files from source to destination with a progress bar
    def copy_files(src_dir, dest_dir):
        # Get the list of all files in the directory
        files = [filename for filename in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, filename))]

        # Initialize tqdm progress bar
        with tqdm(total=len(files), desc=f"Copying {subdirectories} from source to destination", unit="file") as pbar:
            for filename in files:
                src_filepath = os.path.join(src_dir, filename)
                dest_filepath = os.path.join(dest_dir, filename)

                if os.path.exists(dest_filepath):
                    print(f"Overwriting {filename}")

                try:
                    shutil.copy2(src_filepath, dest_filepath)  # Copy file with metadata
                    pbar.update(1)  # Update progress bar after each file copy
                except Exception as e:
                    print(f"Error copying {filename}: {e}")

    # Copy subdirectories (train, test, validation)
    for subdir in subdirectories:
        src_subdir1 = os.path.join(src_dir1, subdir)
        src_subdir2 = os.path.join(src_dir2, subdir)
        dest_subdir = os.path.join(dest_dir, subdir)

        # Ensure the subdirectory exists in the destination
        if not os.path.exists(dest_subdir):
            os.makedirs(dest_subdir)

        # Merge 'images' and 'labels' subdirectories
        for subfolder in ['images', 'labels']:
            if os.path.exists(src_subdir1):
                copy_files(os.path.join(src_subdir1, subfolder), os.path.join(dest_subdir, subfolder))
            if os.path.exists(src_subdir2):
                copy_files(os.path.join(src_subdir2, subfolder), os.path.join(dest_subdir, subfolder))

# Example usage
src_dir1 = './data_aihub_30'
src_dir2 = './data_roboflow'
dest_dir = './merge_dataset'

merge_directories(src_dir1, src_dir2, dest_dir)

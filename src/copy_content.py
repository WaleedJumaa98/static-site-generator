import os
import shutil


def copy_files_recursive(src, dst):
    # First, delete the destination if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # Create the destination directory
    os.mkdir(dst)

    # Get all items in source
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory, recurse
            print(f"Copying directory: {src_path}")
            copy_files_recursive(src_path, dst_path)

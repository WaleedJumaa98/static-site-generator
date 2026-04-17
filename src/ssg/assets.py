import os
import shutil


def copy_files_recursive(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path}")
            copy_files_recursive(src_path, dst_path)

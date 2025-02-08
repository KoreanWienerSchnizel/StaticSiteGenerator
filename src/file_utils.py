import os
import shutil


def copy_directory(source, dest):
    if not os.path.exists(source):
        raise Exception("Source path does not exist")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    print(f"mkdir {dest}")
    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        dest_path = os.path.join(dest, file)
        if os.path.isdir(file_path):
            copy_directory(file_path, dest_path)
        elif os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
            print(f"mv {file_path} {dest_path}")

import os
import shutil
import tempfile
import argparse


def delete_zip_files(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.zip'):
                os.remove(os.path.join(root, file))


def rezip_subfolders(start_path):
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            # Prepare the name for the new zip file
            zip_path = f"{item_path}.zip"
            # Create a temporary directory to hold the contents
            with tempfile.TemporaryDirectory() as temp_dir:
                # Copy the contents of the sub-folder to the temp directory
                for filename in os.listdir(item_path):
                    src_path = os.path.join(item_path, filename)
                    dst_path = os.path.join(temp_dir, filename)
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                # Create a zip file from the temporary directory contents
                shutil.make_archive(base_name=item_path, format='zip', root_dir=temp_dir, base_dir='.')


def main():
    parser = argparse.ArgumentParser(description='Delete .zip files and rezip sub-folders in the given directory.')
    parser.add_argument('path', type=str, help='Path to the directory to process.', nargs='?')

    args = parser.parse_args()

    start_path = args.path

    # if args.path is empty
    if not start_path:
        for dir in os.listdir(os.getcwd()):
            if not os.path.isdir(os.path.join(os.getcwd(), dir)):
                continue
            start_path = os.path.join(os.getcwd(), dir)
            delete_zip_files(start_path)
            rezip_subfolders(start_path)
    # check if start_path exists, if not throw an error
    if not os.path.exists(start_path):
        raise FileNotFoundError(f"Directory {start_path} does not exist")

    delete_zip_files(start_path)
    rezip_subfolders(start_path)

if __name__ == '__main__':
    main()

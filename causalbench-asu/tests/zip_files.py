import argparse
import os
import shutil
import tempfile


def delete_zip_files(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".zip"):
                os.remove(os.path.join(root, file))


def is_module_dir(path):
    return os.path.isfile(os.path.join(path, "config.yaml"))


def list_module_dirs(start_path):
    module_dirs = []
    for root, dirs, files in os.walk(start_path):
        if "config.yaml" in files:
            module_dirs.append(root)
    return module_dirs


def zip_module_dir(module_dir, dry_run=False):
    parent_path = os.path.dirname(module_dir)
    folder_name = os.path.basename(module_dir)
    zip_path = os.path.join(parent_path, folder_name) + ".zip"

    if dry_run:
        print(f"Would create: {zip_path}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy the contents of the module folder to the temp directory
        for filename in os.listdir(module_dir):
            src_path = os.path.join(module_dir, filename)
            dst_path = os.path.join(temp_dir, filename)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
        # Create a zip file from the temporary directory contents
        shutil.make_archive(
            base_name=os.path.join(parent_path, folder_name),
            format="zip",
            root_dir=temp_dir,
            base_dir=".",
        )


def rezip_subfolders(start_path, dry_run=False):
    if is_module_dir(start_path):
        zip_module_dir(start_path, dry_run=dry_run)
        return

    module_dirs = list_module_dirs(start_path)
    if not module_dirs:
        print(f"No modules found under: {start_path}")
        return

    for module_dir in module_dirs:
        zip_module_dir(module_dir, dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(
        description="Delete .zip files and rezip sub-folders in the given directory."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the directory or directories to process (comma-separated for multiple).",
        nargs="?",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be zipped without actually creating zip files.",
    )

    args = parser.parse_args()

    start_path = args.path

    # if args.path is empty, process all directories in current directory
    if not start_path:
        for dir in os.listdir(os.getcwd()):
            if not os.path.isdir(os.path.join(os.getcwd(), dir)):
                continue
            start_path = os.path.join(os.getcwd(), dir)
            if not args.dry_run:
                delete_zip_files(start_path)
            rezip_subfolders(start_path, dry_run=args.dry_run)
    else:
        # Support comma-separated list of directories
        paths = [p.strip() for p in start_path.split(",")]
        for path in paths:
            # check if path exists, if not throw an error
            if not os.path.exists(path):
                raise FileNotFoundError(f"Directory {path} does not exist")

            if not args.dry_run:
                delete_zip_files(path)
            rezip_subfolders(path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

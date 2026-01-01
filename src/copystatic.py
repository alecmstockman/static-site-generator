from pathlib import Path
import shutil
import os


def clear_public_dir(dst):
    project_root = Path(dst).resolve().parent
    destination = dst.resolve()

    if not destination.exists():
        os.makedirs(destination)
    
    if destination.parent != project_root:
        raise RuntimeError("Cannot delete: public is not in project root")
    
    if destination.resolve() == project_root.resolve():
        raise RuntimeError("Refusing to delete project root")
    
    shutil.rmtree(destination)
    destination.mkdir()
     

def copy_files_recursive(src, dst):
    source = Path(src).resolve()
    destination = Path(dst).resolve()

    if not destination.exists():
        os.makedirs(destination)

    for item in os.listdir(source):
        item_path = source / item
        dest_path = destination / item

        if item_path.is_file():
            print(f"- Copying file: {item_path}")
            shutil.copy(item_path, dest_path)

        elif item_path.is_dir():
            print(f"Entering directory: {item_path}")
            copy_files_recursive(item_path, dest_path)

        else:
            print(f"Skipping unknown type: {item_path}")


def copy_static(src, dst):
    clear_public_dir(dst)
    copy_files_recursive(src, dst)





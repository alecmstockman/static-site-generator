from pathlib import Path
from copystatic import copy_static
from gencontent import generate_pages_recursive


def main():
    src = Path("static/")
    dst = Path("public/")
    copy_static(src, dst)
    # print(f"Copied {src} files into {dst} directory")
    generate_pages_recursive("content", "template.html", "public") 
    print("Successfully generated page")


if __name__ == "__main__":
    main()

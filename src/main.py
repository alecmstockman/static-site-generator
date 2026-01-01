from pathlib import Path
from copystatic import copy_static
from gencontent import generate_pages_recursive
import sys


def main():
    src = Path("static/")
    dst = Path("docs/")
    copy_static(src, dst)
    if len(sys.argv) < 2:
        basepath = "/"  
    else:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath) 
    print("Successfully generated page")


if __name__ == "__main__":
    main()

import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.split(" ", 1)[1].strip()
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path, basepath):
    # print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    abs_from = Path(from_path).resolve()
    abs_template = Path(template_path).resolve()
    abs_destination = Path(dest_path).resolve()

    with open(abs_from, "r") as f:
        from_content = f.read()

    with open(abs_template, "r") as f:
        template_content = f.read()

    title = extract_title(from_content)
    content_nodes = markdown_to_html_node(from_content)
    content_html = content_nodes.to_html()

    complete_template = (
        template_content
            .replace("{{ Title }}", title)
            .replace('href="/', 'href="' + basepath)
            .replace('src="/', 'src="' + basepath)
            .replace("{{ Content }}", content_html)
        )

    os.makedirs(abs_destination.parent, exist_ok=True)
    with open(abs_destination, "w", encoding="utf-8") as f:
        f.write(complete_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    abs_content = Path(dir_path_content).resolve()
    template_path = Path(template_path).resolve()
    dest_dir_path = Path(dest_dir_path).resolve()
    content_files = os.listdir(abs_content)
    
    for filename in content_files:
        file_path = os.path.join(abs_content, filename)
        if filename.lower().endswith(".md"):
            destination = Path(dest_dir_path) / filename
            destination = destination.with_suffix(".html")
            generate_page(file_path, template_path, destination, basepath)
        elif os.path.isdir(file_path):
            destination = Path(dest_dir_path) / filename
            generate_pages_recursive(file_path, template_path, destination, basepath)
        else:
            continue
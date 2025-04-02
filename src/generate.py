import os
from os.path import isdir, isfile
from block_utils import extract_title, markdown_to_html_node


def generate_page(source_path, template_path, dest_path, base_path):
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")

    with open(source_path) as f:
        source = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()

    title = extract_title(source)
    source_html = markdown_to_html_node(source).to_html()
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", source_html)
    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)
        f.close()


def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, base_path):
    for file in os.listdir(content_dir_path):
        file_path = os.path.join(content_dir_path, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path, base_path)
        elif os.path.isfile(file_path) and file.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(file_path, template_path, dest_path, base_path)

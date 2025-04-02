import os
import sys
import shutil
from file_utils import copy_directory
from generate import generate_pages_recursive


def main():
    static_dir = "./static"
    public_dir = "./public"
    docs_dir = "./docs"
    content_dir = "./content"
    template_path = "template.html"
    if len(sys.argv) < 2:
        base_path = "/"
    else:
        base_path = sys.argv[1]

    # Generate pages for local testing
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    copy_directory(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir, "/")

    # Generate pages for github pages
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    copy_directory(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, base_path)


if __name__ == "__main__":
    main()

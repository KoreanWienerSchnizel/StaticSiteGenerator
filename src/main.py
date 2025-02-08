import os
import shutil
from file_utils import copy_directory
from generate import generate_page, generate_pages_recursive


def main():
    static_dir = "./static"
    public_dir = "./public"
    content_dir = "./content/"
    template_path = "template.html"

    shutil.rmtree(public_dir)
    copy_directory(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()

from textnode import *
from htmlnode import *
from split import *
import re
import os
import shutil
import sys

def main():
    #test = TextNode("Test", TextType.ITALIC.value, "https://www.boot.dev")
    #print(test.__repr__())
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    static_path = os.getcwd() + "/static"
    public_path = os.getcwd() + "/public"
    copy_from_static(static_path, public_path)
    #generate_page((os.getcwd() + "/content/index.md"), (os.getcwd() + "/template.html"), (public_path + "/index.html"))
    generate_pages_recursive((os.getcwd() + "/content"), (os.getcwd() + "/template.html"), public_path, basepath)


def copy_from_static(static_path, public_path):
    #delete all contents in the public directory first
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    #make new empty public directory
    os.mkdir(public_path)

    items = os.listdir(static_path)
    for item in items:
        item_path = static_path + "/" + item
        new_path = public_path + "/" + item
        if os.path.isfile(item_path):
            shutil.copy((item_path), public_path)
        else:
            os.mkdir(new_path)
            copy_from_static(item_path, new_path)

def extract_title(markdown):
    line_list = markdown.split("\n")
    for line in line_list:
        if line[:2] == "# ":
            return line[2:]
    raise Exception("No h1 tag")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    original = open(from_path).read()
    template = open(template_path).read()

    new_node = markdown_to_html_node(original)
    content = new_node.to_html()

    title = extract_title(original)

    new_file = (template.replace("{{ Title }}", title)).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    f = open(dest_path, "x")
    f.write(new_file)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = dir_path_content + "/" + item
        new_path = dest_dir_path + "/" + item
        if os.path.isfile(item_path):
            if item[-3:] == ".md":
                generate_page(item_path, template_path, new_path[:-3] + ".html", basepath)
        else:
            os.mkdir(new_path)
            generate_pages_recursive(item_path, template_path, new_path, basepath)

main()
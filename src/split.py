from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode(TextType.BOLD.value, text_node.text)
        case TextType.ITALIC:
            return LeafNode(TextType.ITALIC.value, text_node.text)
        case TextType.CODE:
            return LeafNode(TextType.CODE.value, text_node.text)
        case TextType.LINK:
            return LeafNode(TextType.LINK.value, text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(TextType.IMAGE.value, "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        temps = node.text.split(delimiter)
        if len(temps)%2 == 0:
            raise Exception("Not valid markdown syntax")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        for temp in temps:
            if (f"{delimiter}{temp}{delimiter}") in node.text: #If necessary, This line can be fixed by only working if the index of the list entry is odd
                temp_node = TextNode(temp, text_type)
            else:
                temp_node = TextNode(temp, TextType.TEXT)
            new_nodes.append(temp_node)
    return new_nodes

def extract_markdown_images(text):
    img = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img

def extract_markdown_links(text):
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    starter = [] 
    starter.append(TextNode(text, TextType.TEXT))
    temp = split_nodes_delimiter(starter, "**", TextType.BOLD)
    temp = split_nodes_delimiter(temp, "_", TextType.ITALIC)
    temp = split_nodes_delimiter(temp, "`", TextType.CODE)
    final = split_nodes_image(temp)
    final = split_nodes_link(final)
    return final

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        lines = block.split("\n")
        strip_line = []
        for line in lines:
            temp_line = line.strip()
            if temp_line:
                strip_line.append(temp_line)
        temp_block = "\n".join(strip_line)
        if temp_block:
            new_blocks.append(temp_block)
    return new_blocks

from enum import Enum

class BlockType(Enum):
    paragraph = ""
    heading = "# "
    code = "`"
    quote = ">"
    unordered_list = "- "
    ordered_list = "#. "

def block_to_block_type(block):
    #list tests
    is_unordered = False
    is_ordered = False
    lines = block.split("\n")
    if block.startswith("- "):
        is_unordered = True
        for line in lines:
            if line.startswith("- ") == False:
                is_unordered = False  
    elif block.startswith("1. "):
        is_ordered = True
        i = 1
        for line in lines:
            if line.startswith(f"{i}. ") == False:
                print(f"invalid line: {line}")
                is_ordered = False
            i+= 1

    
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    elif block[0] == ">":
        return BlockType.quote
    elif is_unordered:
        return BlockType.unordered_list
    elif is_ordered:
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

def markdown_to_html_node(markdown): #only thing im missing are urls/links
    blocks = markdown_to_blocks(markdown)
    new_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.heading:
            head_num = 0
            for char in block:
                if char == "#":
                    head_num += 1
            node = ParentNode(f"h{head_num}", text_to_children(block.lstrip("#").lstrip(), block_type))
        elif block_type == BlockType.code:
            code_text = TextNode((block.rstrip("```")).lstrip("```\n"), TextType.CODE)
            node = ParentNode("pre", [text_node_to_html_node(code_text)])
        elif block_type == BlockType.quote:
            node = ParentNode("blockquote", text_to_children(block, block_type))
        elif block_type == BlockType.unordered_list:
            node = ParentNode("ul", text_to_children(block, block_type))
        elif block_type == BlockType.ordered_list:
            node = ParentNode("ol", text_to_children(block, block_type))
        elif block_type == BlockType.paragraph:
            node = ParentNode("p", text_to_children(block, block_type))
        else:
            raise Exception("Invalid block type")
        new_nodes.append(node)
    parent = ParentNode("div", new_nodes)
    return parent

def text_to_children(block, block_type):
    new_block = block.replace("\n", " ")
    new_nodes = []

    if block_type == BlockType.unordered_list or block_type == BlockType.ordered_list:
        if block_type == BlockType.unordered_list:
            listed = new_block.split("- ")
        else:
            listed = re.split(r"\d+\.\s", new_block)
        for item in listed[1:]:
            new_list_nodes = []
            lnodes = text_to_textnodes(item.strip())
            for lnode in lnodes:
                new_list_nodes.append(text_node_to_html_node(lnode))
            list_node = ParentNode("li", new_list_nodes)
            new_nodes.append(list_node)
    else: #regular case
        if(block_type == BlockType.quote):
            nodes = text_to_textnodes(new_block.replace(">", "").lstrip())
        else:
            nodes = text_to_textnodes(new_block)
        for node in nodes:
            new_nodes.append(text_node_to_html_node(node))
           # print (text_node_to_html_node(node).to_html())
    return new_nodes

#def list_split(block, block_type) #shouldnt need this
    

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode, HTMLNode
import re
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes value must be a list")

    for node in old_nodes:
        new_node = []
        sections = node.text.split(delimiter)

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, unmatched delimiter")
        
        if text_type == TextType.BOLD:
            inner_type = TextType.BOLD
        elif text_type == TextType.ITALIC:
            inner_type = TextType.ITALIC
        elif text_type == TextType.CODE:
            inner_type = TextType.CODE
        else:
            raise ValueError(f"Unsupported text_type: {text_type}")
        
        for index, section in enumerate(sections):
            if section == "":
                continue
            elif index % 2 == 0:
                new_node.append(TextNode(section, TextType.TEXT))
            else:
                new_node.append(TextNode(section, inner_type))
        new_nodes.extend(new_node)
    return new_nodes


def extract_markdown_images(text):
    text_url_list =  re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_url_list


def extract_markdown_links(text):
    markdown_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return markdown_link


def split_nodes_images(old_nodes):
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if original_text == "":
            continue
        if extract_markdown_images(original_text) == []:
            new_nodes.append(node)
            continue

        node_sections = []
        image_alt_and_urls = extract_markdown_images(original_text)
        text = original_text
        for image in image_alt_and_urls:
            image_alt = image[0]
            image_link = image[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != '':
                node_sections.append(TextNode(f"{sections[0]}", TextType.TEXT))
            node_sections.append(TextNode(f"{image_alt}", TextType.IMAGE, f"{image_link}"))
            text = sections[1]
        if text != "":
            node_sections.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(node_sections)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # print(node)
        original_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if original_text == "":
            continue
        if extract_markdown_links(original_text) == []:
            new_nodes.append(node)
            continue

        node_sections = []
        link_desc_and_urls = extract_markdown_links(original_text)
        text = original_text
        for link in link_desc_and_urls:
            link_desc = link[0]
            link_url = link[1]
            sections = text.split(f"[{link_desc}]({link_url})", 1)
            if sections[0] != '':
                node_sections.append(TextNode(f"{sections[0]}", TextType.TEXT))
            node_sections.append(TextNode(f"{link_desc}", TextType.LINK, f"{link_url}"))
            text = sections[1]
        if text != "":
            node_sections.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(node_sections)
    return new_nodes


def text_to_textnode(text):
    text_node = TextNode(text, TextType.TEXT)
    split_code_result = split_nodes_delimiter([text_node], "`", TextType.CODE)
    split_bold_result = split_nodes_delimiter(split_code_result, "**", TextType.BOLD)
    split_italic_result = split_nodes_delimiter(split_bold_result, "_", TextType.ITALIC)
    split_images_result = split_nodes_images(split_italic_result)
    return split_nodes_links(split_images_result)


def markdown_to_blocks(text):
    split_lines = text.split("\n\n")
    block = []
    for line in split_lines:
        if line != "":
            block.append(line.strip())
    return(block)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_blocktype(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = [line for line in block.strip().split("\n") if line]

    if all(re.match(r"^\>", line) for line in lines):
        return BlockType.QUOTE

    if all(re.match(r"^\-+\s", line) for line in lines):
        return BlockType.UNORDERED_LIST

    lines = [line for line in block.strip().split("\n") if line]
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def blocktype_to_tag(block):
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARAGRAPH:
        tag = "p"
    if block_type == BlockType.HEADING:
        block_start = block.split(" ", 1)
        tag = f"h{block_start[0].count('#')}"
    if block_type == BlockType.CODE:
        tag = "code"
    if block_type == BlockType.QUOTE:
        tag = "q"
    if block_type == BlockType.UNORDERED_LIST:
        tag = "ul"
    if block_type == BlockType.ORDERED_LIST:
        tag = "ol"
    return tag


def remove_block_header(block, blocktype):
    if blocktype == BlockType.HEADING:
        return block.split("# ", 1)[1]
    
    if blocktype == BlockType.QUOTE:
        return block.split(">", 1)[1]
    
    if blocktype == BlockType.UNORDERED_LIST:
        items = block.split("\n")[1:-1]
        return "\n".join(item.split("- ", 1)[1] for item in items)
    
    if blocktype == BlockType.ORDERED_LIST:
        ordered_list = block.split("\n")[1:-1]
        return "\n".join(re.sub(r"^\d+\.\s", "", item) for item in ordered_list)
    
    else:
        return block


# print(remove_block_header(blk, BlockType.ORDERED_LIST))



md = """
## Header: The Two Towers!

>BLAH BLAH BLAH

- List 
"""

"""
**bolded text lies here**

```CODE: One Ring to Rule Them All```

This is a paragraph of text \nAnd here is another line
"""



txt = "### Header"

def text_to_children(text):
    children = []
    textnodes = text_to_textnode(text)
    for node in textnodes:
        leafnode = text_node_to_html_node(node)
        children.append(leafnode)
    return children




def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parentnodes = []
    for block in blocks:
        if block == "":
            continue
        # print("block:", block)
        blocktype = block_to_blocktype(block)
        print("--- blocktype:", blocktype)
        stripped_block = remove_block_header(block, blocktype)

        print(f"stripped_block: {stripped_block}")
        tag = blocktype_to_tag(block)
        # print("--- Blocktype:", blocktype, "\n")
        # print("--- Tag:", tag)
        if blocktype != BlockType.CODE:
            children = text_to_children(stripped_block)
            print("---", children, "\n")
        else:
            code_block = text_to_textnode(stripped_block)
            tag = 'pre'
            # print("---", code_block)
            children = [HTMLNode(tag='code', value=code_block[0].text, children=None, props={})]
            # print("\n")
        
        parent = HTMLNode(tag, value=None, children=children,)
        parentnodes.append(parent)

    root_node = HTMLNode(tag=None, value=None, children=parentnodes)
    return root_node


results = markdown_to_html_node(md)
print(results)










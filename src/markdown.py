from textnode import TextNode, TextType
import re

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
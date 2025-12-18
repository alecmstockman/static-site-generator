from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        new_node = []

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
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

            if index == 0 and section == "":
                continue
            elif index % 2 == 0:
                new_node.append(TextNode(section, TextType.TEXT))
            else:
                new_node.append(TextNode(section, inner_type))

        new_nodes.extend(new_node)
    return new_nodes




# bold_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

# for n in bold_nodes:
#     print(n)
# bold_texts = [node.text for node in bold_nodes if node.text_type == TextType.BOLD]
# print(bold_texts)



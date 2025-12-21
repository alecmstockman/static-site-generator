import unittest
from markdown import BlockType, block_to_blocktype, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnode, markdown_to_blocks
from textnode import TextNode, TextType
import textwrap

class TestMarkdown(unittest.TestCase):
    def setUp(self):
        self.original_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT), 
            TextNode("This is text with a **bold words block** word", TextType.TEXT), 
            TextNode("**This** is text with two **bold words** blocks", TextType.TEXT), 
            TextNode("This is text with a _italic_ block word", TextType.TEXT)
            ]
        self.nodes = self.original_nodes.copy()

        self.original_image_nodes = [
            TextNode("", TextType.TEXT,), 
            TextNode("This is text", TextType.TEXT,), 
            TextNode("This is text and ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT,), 
            TextNode("This is text and [rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT,),
            TextNode("This is text and ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.BOLD,), 
            TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) Random Text Here", TextType.TEXT,), 
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT,), 
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT,)
            ]
        self.image_nodes = self.original_image_nodes.copy()

        self.original_link_nodes = [
            TextNode("", TextType.TEXT,), 
            TextNode("This is text", TextType.TEXT,), 
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT,), 
            TextNode("This is text with a link ![to boot dev](https://www.boot.dev)", TextType.TEXT,), 
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.BOLD,), 
            TextNode("This is text with a link ![to boot dev](https://www.boot.dev)", TextType.BOLD,), 
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,), 
            TextNode("[to boot dev](https://www.boot.dev) and another link: [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,), 
            TextNode("This is text a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT, ), 
            TextNode("[to boot dev](https://www.boot.dev) Random Text Here", TextType.TEXT,), 
            ]
        self.link_nodes = self.original_link_nodes.copy()

        self.original_split_lines_text = textwrap.dedent("""
            # This is a heading

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

            - This is the first list item in a list block
            - This is a list item
            - This is another list item
        """).strip()

        self.split_lines_text = self.original_split_lines_text



    def tearDown(self):
        self.nodes = self.original_nodes.copy()
        self.image_nodes = self.original_image_nodes.copy()
        self.original_link_nodes = self.original_image_nodes.copy()

    def test_bold(self):
        split_node = split_nodes_delimiter(self.nodes, '**', TextType.BOLD)
        self.assertEqual(
            split_node, [
                TextNode("This is text with a `code block` word", TextType.TEXT, None), 
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("bold words block", TextType.BOLD, None), 
                TextNode(" word", TextType.TEXT, None), 
                TextNode("This", TextType.BOLD, None), 
                TextNode(" is text with two ", TextType.TEXT, None), 
                TextNode("bold words", TextType.BOLD, None), 
                TextNode(" blocks", TextType.TEXT, None), 
                TextNode("This is text with a _italic_ block word", TextType.TEXT, None)
                ]
            )
        
    def test_one_bold_word(self):
        n = TextNode("**bold**", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(split_node, [TextNode("bold", TextType.BOLD, None)])

    def test_one_bold_word_adjacent_word(self):
        n = TextNode("There is one **bold**word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(
            split_node, [
                TextNode("There is one ", TextType.TEXT, None), 
                TextNode("bold", TextType.BOLD, None), 
                TextNode("word", TextType.TEXT, None)
                ]
                )

    def test_not_equal_bold_word_one_delimiter(self):
        n = TextNode("This is a **bold word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([n], "**", TextType.TEXT)
        self.assertIn("Invalid markdown, unmatched delimiter", str(cm.exception))

    def test_two_bold_words(self):
        n = TextNode("**bold** word is a **bold** word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(
            split_node, [
                TextNode("bold", TextType.BOLD, None), 
                TextNode(" word is a ", TextType.TEXT, None), 
                TextNode("bold", TextType.BOLD, None), 
                TextNode(" word", TextType.TEXT, None)
                ]
                )
        
    def test_two_bold_words_together(self):
        n = TextNode("**bold** **word** is a bold word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(
            split_node, [
                TextNode("bold", TextType.BOLD, None), 
                TextNode(" ", TextType.TEXT, None), 
                TextNode("word", TextType.BOLD, None), 
                TextNode(" is a bold word", TextType.TEXT, None)
                ]
                )

    def test_italic_with_bold(self):
        n = TextNode("**bold** and _italic_ word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '_', TextType.ITALIC)
        self.assertEqual(
            split_node, [
                TextNode("**bold** and ", TextType.TEXT, None), 
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(" word", TextType.TEXT, None)
                ]
                )

    def test_code(self):
        split_node = split_nodes_delimiter(self.nodes, '`', TextType.CODE)
        self.assertEqual(
            split_node, [
                TextNode("This is text with a ", TextType.TEXT, None), 
                TextNode("code block", TextType.CODE, None), 
                TextNode(" word", TextType.TEXT, None), 
                TextNode("This is text with a **bold words block** word", TextType.TEXT, None), 
                TextNode("**This** is text with two **bold words** blocks", TextType.TEXT, None), 
                TextNode("This is text with a _italic_ block word", TextType.TEXT, None)
                ]
                )
        
    def test_two_code_words(self):
        n = TextNode("`bold` word is a `bold` word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '`', TextType.CODE)
        self.assertEqual(
            split_node, [
                TextNode("bold", TextType.CODE, None), 
                TextNode(" word is a ", TextType.TEXT, None),
                TextNode("bold", TextType.CODE, None), 
                TextNode(" word", TextType.TEXT, None)
                ]
                )
        
    def test_italic(self):
        split_node = split_nodes_delimiter(self.nodes, '_', TextType.ITALIC)
        self.assertEqual(
            split_node, [
                TextNode("This is text with a `code block` word", TextType.TEXT, None), 
                TextNode("This is text with a **bold words block** word", TextType.TEXT, None), 
                TextNode("**This** is text with two **bold words** blocks", TextType.TEXT, None), 
                TextNode("This is text with a ", TextType.TEXT, None), 
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(" block word", TextType.TEXT, None)
                ]
                )

    def test_two_italic_words(self):
        n = TextNode("_italic_ word is a _italic_ word", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '_', TextType.ITALIC)
        self.assertEqual(
            split_node, [
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(" word is a ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(" word", TextType.TEXT, None)
                ]
                )

    def test_no_delimiter(self):
        node = TextNode("This is text with one code block` word and another `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "", TextType.TEXT)
        self.assertIn("empty separator", str(cm.exception))

    def test_old_nodes_invalid_text_type(self):
        node = TextNode("This is text with one code block` word and another `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "_", TextType.TEXT)
        self.assertIn(f"Unsupported text_type: {node.text_type}", str(cm.exception))

    def test_non_text_nodes_untouched(self):
        n = TextNode("**already bold**", TextType.BOLD)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(split_node, [n])

    def test_multiple_text_nodes_each_split(self):
        n1 = TextNode("One `code` here", TextType.TEXT)
        n2 = TextNode("And `code` there", TextType.TEXT)
        split_node = split_nodes_delimiter([n1, n2], '`', TextType.CODE)
        self.assertEqual(
            split_node,
            [
                TextNode("One ", TextType.TEXT, None),
                TextNode("code", TextType.CODE, None),
                TextNode(" here", TextType.TEXT, None),
                TextNode("And ", TextType.TEXT, None),
                TextNode("code", TextType.CODE, None),
                TextNode(" there", TextType.TEXT, None),
            ],
        )

    def test_unmatched_closing_delimiter(self):
        n = TextNode("This is a bold** word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([n], "**", TextType.BOLD)

    def test_delimiter_at_start_with_trailing_text(self):
        n = TextNode("**bold** and more", TextType.TEXT)
        split_node = split_nodes_delimiter([n], '**', TextType.BOLD)
        self.assertEqual(
            split_node,
            [
                TextNode("bold", TextType.BOLD, None),
                TextNode(" and more", TextType.TEXT, None),
            ],
        )

    def test_multiple_split_node_delimiter(self):
        n = TextNode("There text has a **bold**, _italic_, and a `code` word", TextType.TEXT)
        nodes = [n]
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            nodes, [
                TextNode("There text has a ", TextType.TEXT, None), 
                TextNode("bold", TextType.BOLD, None), 
                TextNode(", ", TextType.TEXT, None), 
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(", and a ", TextType.TEXT, None), 
                TextNode("code", TextType.CODE, None), 
                TextNode(" word", TextType.TEXT, None)
                ]
            )

    def test_markdown_images(self):
        image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_images = extract_markdown_images(image_text)
        self.assertEqual(markdown_images, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_markdown_links(self):
        link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        markdown_images = extract_markdown_links(link_text)
        self.assertEqual(markdown_images, [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

    def test_no_images(self):
        text = "Just some text with no images or links."
        self.assertEqual(extract_markdown_images(text), [])

    def test_no_links(self):
        text = "Just some text with ![an image](https://img.com/x.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_images_not_counted_as_links(self):
        text = "Look ![alt](https://img.com/x.png) and [link](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")]
        )

    def test_mixed_images_and_links(self):
        text = "![img1](url1) [link1](url2) ![img2](url3) [link2](url4)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img1", "url1"), ("img2", "url3")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link1", "url2"), ("link2", "url4")]
        )

    def test_empty_alt_and_link_text(self):
        text = "![](img.png) [](link.html)"
        self.assertEqual(extract_markdown_images(text), [("", "img.png")])
        self.assertEqual(extract_markdown_links(text), [("", "link.html")])


# -------- SPLIT NODES IMAGES --------

    def test_split_nodes_images(self):
        split_images = split_nodes_images(self.original_image_nodes)
        self.assertEqual(
            split_images, [                
                TextNode("This is text", TextType.TEXT, None), 
                TextNode("This is text and ", TextType.TEXT, None), 
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                TextNode("This is text and [rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT, None), 
                TextNode("This is text and ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.BOLD, None), 
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                TextNode(" Random Text Here", TextType.TEXT, None), 
                TextNode("This is text with a ", TextType.TEXT, None), 
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                TextNode(" and ", TextType.TEXT, None), 
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT, None), 
                ]
            )


# -------- SPLIT NODES LINKS --------

    def test_split_nodes_links(self):
        split_links = split_nodes_links(self.original_link_nodes)
        self.assertEqual(
            split_links, 
               [
                TextNode("This is text", TextType.TEXT, None), 
                TextNode("This is text with a link ", TextType.TEXT, None), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode("This is text with a link ![to boot dev](https://www.boot.dev)", TextType.TEXT, None), 
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.BOLD, None), 
                TextNode("This is text with a link ![to boot dev](https://www.boot.dev)", TextType.BOLD, None), 
                TextNode("This is text with a link ", TextType.TEXT, None), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" and ", TextType.TEXT, None), 
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" and another link: ", TextType.TEXT, None), 
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
                TextNode("This is text a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT, None), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" Random Text Here", TextType.TEXT, None)
                ]
            )


# -------- FULL MAKRDONW TO TEXTNODE  --------

    def test_of_text_to_textnode(self):
        final_node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnode(final_node)
        self.assertEqual(
            result, [
                TextNode("This is ", TextType.TEXT, None), 
                TextNode("text", TextType.BOLD, None), 
                TextNode(" with an ", TextType.TEXT, None), 
                TextNode("italic", TextType.ITALIC, None), 
                TextNode(" word and a ", TextType.TEXT, None), 
                TextNode("code block", TextType.CODE, None), 
                TextNode(" and an ", TextType.TEXT, None), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", TextType.TEXT, None), 
                TextNode("link", TextType.LINK, "https://boot.dev"), 
                ] 
            )
    

# -------- FULL MAKRDONW TO BLOCKS --------

    def test_markdown_to_blocks(self):
        block_text = markdown_to_blocks(self.original_split_lines_text)
        self.assertEqual(
            block_text, [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', 
                '- This is the first list item in a list block\n- This is a list item\n- This is another list item'
                ]
                )
        
# -------- BLOCK TO BLOCKTYPE  --------

    def test_blocktype_heading(self):
        heading_text = "# Some heading text here"
        self.assertEqual(BlockType.HEADING, block_to_blocktype(heading_text))
    
    def test_blocktype_heading_six(self):
        heading_text_six = "###### Some heading text here"
        self.assertEqual(BlockType.HEADING, block_to_blocktype(heading_text_six))

    def test_notequal_blocktype_heading_no_space(self):
        heading_text_no_space = "###Some heading text here"
        self.assertNotEqual(BlockType.HEADING, block_to_blocktype(heading_text_no_space))

    def test_notequal_blocktype_heading_seven(self):
        heading_text_seven = "####### Some heading text here"
        self.assertNotEqual(BlockType.HEADING, block_to_blocktype(heading_text_seven))


    def test_blocktype_code(self):
        code_text = "```This is a code block```"
        self.assertEqual(BlockType.CODE, block_to_blocktype(code_text))

    def test_blocktype_code_spaces(self):
        code_text_spaces = "``` This is a code block ```"
        self.assertEqual(BlockType.CODE, block_to_blocktype(code_text_spaces))

    def test_blocktype_code_no_postfix(self):
        code_text_no_postfix = "```This is a code block"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(code_text_no_postfix))

    def test_blocktype_code_no_prefix(self):
        code_text_no_prefix = "This is a code block```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(code_text_no_prefix))


    def test_blocktype_quote(self):
        quote_text = ">This is a quote block"
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_text))

    def test_blocktype_quote_multiple_lines(self):
        quote_text_mulitple = ">This is a quote block \n>More Text \n>Even more Text"
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_text_mulitple))

    def test_blocktype_quote_empty_line(self):
        quote_text_empty_line = ">This is a quote block \n\n>More Text \n>Even more Text"
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_text_empty_line))

    def test_blocktype_quote_paragraph(self):
        quote_text_paragraph = "This is a quote block"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(quote_text_paragraph))

    def test_notequal_blocktype_quote_wrong_symbol(self):
        quote_text_wrong = "<This is a quote block"
        self.assertNotEqual(BlockType.QUOTE, block_to_blocktype(quote_text_wrong))


    def test_blocktype_unordered(self):
        unordered_text = "- Aragon, Gimli, Legolas, Frodo, Sam, Pippin, Merry"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(unordered_text))

    def test_blocktype_unordered_multiple_lines(self):
        unordered_text_multi_line = "- Aragon \n- Gimli\n- Legolas\n- Frodo\n- Sam\n- Pippin\n- Merry"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(unordered_text_multi_line))

    def test_blocktype_unordered_no_space(self):
        unordered_text_no_space = "- Aragon \n-Gimli\n- Legolas\n- Frodo\n- Sam\n- Pippin\n- Merry"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(unordered_text_no_space))

    def test_notequal_blocktype_unordered(self):
        unordered_text = "- Aragon \n- Gimli\n- Legolas\n- Frodo\n- Sam\n- Pippin\n Merry"
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_blocktype(unordered_text))

    def test_blocktype_unordered_with_blank_line(self):
        text = "- one\n\n- two"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(text))
    

    def test_blocktype_ordered(self):
        ordered_text = "1. First line in the list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(ordered_text))

    def test_blocktype_ordered_two_lines(self):
        ordered_text_two_lines = "1. First line in the list \n2. Second Line"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(ordered_text_two_lines))

    def test_blocktype_ordered_multi_lines(self):
        ordered_text_multi_line = "1. First line in the list \n2. Second Line\n3. Third Line"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(ordered_text_multi_line))

    def test_blocktype_missing_dot(self):
        ordered_text_missing_dot = "1. First line in the list \n2 Second Line\n3. Third Line"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(ordered_text_missing_dot))

    def test_blocktype_ordered_wrong_increment(self):
        text = "1. one\n3. three"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text))

    def test_blocktype_ordered_with_blank_line(self):
        text = "1. one\n\n2. two"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(text))


    def test_blocktype_paragraph(self):
        paragraph = "This is just normal text"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(paragraph))

    def test_blocktype_paragraph_empty(self):
        paragraph_empty = ""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(paragraph_empty))



# heading_text = "## Some heading text here"
# code_text = "```This is a code block```"
# quote_text = ">This is a quote block"
# unordered_text = "- Aragon, Gimli, Legolas, Frodo, Sam, Pippin, Merry"
# ordered_text = "1. First line in the list \n2. Second Line"
import unittest
from markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkdown(unittest.TestCase):
    def SetUp(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT), 
            TextNode("This is text with a **bold words block** word", TextType.TEXT), 
            TextNode("**This** is text with two **bold words** blocks", TextType.TEXT), 
            TextNode("This is text with a _italic_ block word", TextType.TEXT)
            ]

    def test_code_one_block(self):
        # node = TextNode("This is text with a `code block` word", TextType.TEXT)
        split_node = split_nodes_delimiter(node, '`', TextType.TEXT)
        self.assertEqual(split_node,
        [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)])

    # def test_code_two_blocks(self):
    #     node = TextNode("This is text with one `code block` word and another `code block` word", TextType.TEXT)
    #     split_node = split_nodes_delimiter(node, '`', TextType.TEXT)
    #     self.assertEqual(
    #         split_node, [
    #             TextNode("This is text with one ", TextType.TEXT, None), 
    #             TextNode("code block", TextType.CODE, None), 
    #             TextNode(" word and another ", TextType.TEXT, None), 
    #             TextNode("code block", TextType.CODE, None), 
    #             TextNode(" word", TextType.TEXT, None)
    #             ]
    #             )

    # def test_code_two_blocks_invalid(self):
    #     node = TextNode("This is text with one code block` word and another `code block` word", TextType.TEXT)
    #     with self.assertRaises(Exception) as cm:
    #         split_nodes_delimiter(node, '`', TextType.TEXT)
    #     self.assertIn("Invalid markdown text", str(cm.exception))


import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_not_text(self):
        node = TextNode("Testing, testing, testing...", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_text_type_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text_type_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_same_urls(self):
        node = TextNode("This is a different text node", TextType.CODE, "http://boot.dev")
        node2 = TextNode("This is a different text node", TextType.CODE, "http://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_urls(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a different text node", TextType.ITALIC, None)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq_url_none(self):
        node = TextNode("This is a different text node", TextType.ITALIC, None)
        node2 = TextNode("This is a different text node", TextType.ITALIC, "http://boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("alt text here", TextType.IMAGE, "https://www.google.com/image.png",)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com/image.png", "alt": "alt text here"},)

    def test_invalid_type_raises(self):
        class FakeType: pass
        node = TextNode("x", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
    
import unittest
from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()
    
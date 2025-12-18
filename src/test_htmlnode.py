import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def setUp(self):
        self.node1 = HTMLNode("a", "One ring to rule them all")
        self.node2 = HTMLNode("p", "One ring to find them", None, props={"href": "http://boot.dev", "src": "image.png"})
        self.node3 = HTMLNode("h1", "One ring to bring them all")
        self.node4 = HTMLNode("img", "and in the darkness, bind them", None, props=None)

    def test_props_none(self):
        self.assertEqual(self.node1.props_to_html(), "")

    def test_props_to_html_multiple(self):
        self.assertEqual(self.node2.props_to_html(), ' href="http://boot.dev" src="image.png"')
    
    def test_children_stored(self):
        child = self.node1
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children, [child])

    def test_props_none_on_h1(self):
        self.assertEqual(self.node3.props_to_html(), "")

    def test_props_empty_dict(self):
        node = HTMLNode("a", "test", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.node1.to_html()

    def test_constructor_sets_fields(self):
        children = [self.node1, self.node2]
        props = {"class": "ring"}
        node = HTMLNode("div", "Mordor", children=children, props=props)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Mordor")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        repr(self.node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hi, planet!")
        self.assertEqual(node.to_html(), "<a>Hi, planet!</a>")

    def test_leaf_to_html_not_a(self):
        node = LeafNode("a", "Hi, planet!")
        self.assertNotEqual(node.to_html(), "<b>Hi, planet!</b>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
            )
        
    def test_leaf_to_html_raises_when_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_child_no_child(self):
        child_node = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node])

        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "children must have a value")
            
    def test_to_html_grandchild_no_child(self):
        child_node = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node])

        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "children must have a value")



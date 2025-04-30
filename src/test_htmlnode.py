import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_prop(self):
        node = HTMLNode("a", "This is a link test", [], {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com"')

    def test_prop_2(self):
        node = HTMLNode("a", "This is a link test", [], {"href": "https://www.google.com", "test": "https://www.youtube.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" test="https://www.youtube.com"')

    def test_display(self):
        node = HTMLNode("a", "This is a link test", [], {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(), "tag:a, value:This is a link test, children:[], props: {'href': 'https://www.google.com'}")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_parent_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
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
    
    #def test_none(self):
       # node = HTMLNode()
        #print(node.props_to_html())
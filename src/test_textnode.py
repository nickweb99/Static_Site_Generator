import unittest

from textnode import *
from main import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("", TextType.CODE, "https://github.com/nickweb99/Static_Site_Generator")
        node2 = TextNode("", TextType.CODE, "https://github.com/nickweb99/Static_Site_Generator")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.CODE, "https://github.com/nickweb99/Static_Site_Generator")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_disp(self):
        node = TextNode("This is a text node", TextType.CODE, "https://github.com/nickweb99/Static_Site_Generator")
        node_rep = (f"TextNode({node.text}, {node.text_type}, {node.url})")
        self.assertEqual(node.__repr__(), node_rep)

    

if __name__ == "__main__":
    unittest.main()
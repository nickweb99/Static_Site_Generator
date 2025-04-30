import unittest

from textnode import *
from split import *


class TestSplit(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_delimiter(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        #print(f"Delimeter: {split_nodes_delimiter([node],"**", TextType.BOLD)}")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_textnode_final_creation(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test_nodes = text_to_textnodes(text)
        #print(f"textnodes: {test_nodes}")
        self.assertListEqual(
            [
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
            ],
            test_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_type(self):
        block = ">This is a quote block"
        test = block_to_block_type(block)
        self.assertEqual(
            test, BlockType.quote
        )

        block2 = "```This is a code block```"
        test2 = block_to_block_type(block2)
        self.assertEqual(
            test2, BlockType.code
        )

        block3 = "- This is an\n- unordered\n- list"
        test3 = block_to_block_type(block3)
        self.assertEqual(
            test3, BlockType.unordered_list
        )

        block4 = "1. This is an\n2. unordered\n3. list"
        test4 = block_to_block_type(block4)
        self.assertEqual(
            test4, BlockType.ordered_list
        )

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all_markdown(self):
        md = """
        # Tolkien Fan Club

        ![JRR Tolkien sitting](/images/tolkien.png)

        Here's the deal, **I like Tolkien**.

        > "I am in fact a Hobbit in all but size."
        >
        > -- J.R.R. Tolkien

        ## Blog posts

        - [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
        - [Why Tom Bombadil Was a Mistake](/blog/tom)
        - [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

        ## Reasons I like Tolkien

        - You can spend years studying the legendarium and still not understand its depths
        - It can be enjoyed by children and adults alike
        - Disney _didn't ruin it_ (okay, but Amazon might have)
        - It created an entirely new genre of fantasy

        ## My favorite characters (in order)

        1. Gandalf
        2. Bilbo
        3. Sam
        4. Glorfindel
        5. Galadriel
        6. Elrond
        7. Thorin
        8. Sauron
        9. Aragorn

        Here's what `elflang` looks like (the perfect coding language):

        ```
        func main(){
            fmt.Println("Aiya, Ambar!")
        }
        ```

        Want to get in touch? [Contact me here](/contact).

        This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        # self.assertEqual(
        #     html,
        #     "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        # )
        print(html)

if __name__ == "__main__":
    unittest.main()
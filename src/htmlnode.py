class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not implemented in parent")

    def props_to_html(self):
        temp = ""
        if self.props == None:
            #raise Exception("No properties")
            print("No properties")
        for item in self.props:
            temp += (f'{item}="{self.props[item]}" ')
        return temp.strip()

    def __repr__(self):
        return (f"tag:{self.tag}, value:{self.value}, children:{self.children}, props: {self.props}")
        
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value = None, props = None):
        super().__init__(tag, value, children = None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Must have a value")
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f'<{self.tag} src="{self.props["src"]}" alt="{self.props["alt"]}">'
        if self.tag == "a":
            return f'<{self.tag} href="{self.props["href"]}">{self.value}</{self.tag}>'

        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children = None, props = None):
        super().__init__(tag, value = None, children = children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Must have a tag")
        if self.children == None:
            raise ValueError("Must have a child")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()

        return f"<{self.tag}>{child_html}</{self.tag}>"
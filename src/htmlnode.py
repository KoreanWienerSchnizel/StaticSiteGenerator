class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props={}):
        self.value = value
        self.tag = tag
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        for k, v in self.props.items():
            html_string += f' {k}="{v}"'
        return html_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode Error: no value")
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode Error: no tag")
        if not self.children:
            raise ValueError("ParentNode Error: no children")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += f"{child.to_html()}"
        html_string += f"</{self.tag}>"
        return html_string

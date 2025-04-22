from enum import Enum
from textnode import *

class HTMLNode:

    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("This method must be overridden by subclasses")
    
    def props_to_html(self):
        attribute_string = ""
        if self.props != None:
            for key,value in self.props.items():
                attribute_string = attribute_string+" "+key+"="+'"'+value+'"'
        return attribute_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None,props)

    def to_html(self):
        if self.tag is None:
            return self.value or ""
            
        # For leaf nodes (no children)
        if self.children is None:
            if self.value is None:
                return f"<{self.tag}{self.props_to_html()}/>"  # Self-closing tag
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        # For nodes with children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
            
        # Special case for leaf nodes (no children, just value)
        if self.children is None:
            if self.value is None:
                return f"<{self.tag}{self.props_to_html()}/>"  # Self-closing tag
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        # For nodes with children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        
        
        


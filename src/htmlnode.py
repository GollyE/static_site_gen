
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
        for key,value in self.props.items():
            attribute_string = attribute_string+" "+key+"="+'"'+value+'"'
        return attribute_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
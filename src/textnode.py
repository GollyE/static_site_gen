from enum import Enum


class TextType(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINKS = 5
    IMAGES = 6

class TextNode: 

    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_text_node):
        return (
            self.text == other_text_node.text and 
            self.text_type == other_text_node.text_type and 
            self.url == other_text_node.url
            )

    

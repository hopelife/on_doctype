# -*- coding=utf-8 -*-
"""
Implements: 
    [X] 
    [] 

Usages: 
    - 

Requirements:
    - pip install 

References:
    - [plantuml](https://plantuml.com/ko/)
    - [kroki](https://kroki.io/)
    - [plantuml github](https://github.com/plantuml/plantuml)
    - [python-plantuml github](https://github.com/dougn/python-plantuml/)
    - [PlantUMLDesignPatterns github](https://github.com/RafaelKuebler/PlantUMLDesignPatterns)
    - [Real World PlantUML](https://real-world-plantuml.com/)
    - [PlantUML](https://programmersought.com/article/14924735989/)
    - [OSCIED/docs/david/uml/](https://github.com/ebu/OSCIED/tree/7eebadfef2a47c55db0cdc1a2e4c653a613e27ec/docs/david/uml)


Cautions:
    - 

Created:
    - by:
    - started:  
    - updated: 
     
"""

##@@@ Import AREA
##============================================================

##@@ Built-In Modules
##------------------------------------------------------------
# from email.headerregistry import DateHeader
import os, sys
import zlib
import base64
import string

##@@ Installed Modules
##------------------------------------------------------------
# from on_database.db_mysql import Mysql
# from on_builtin.util_data import (_to_lists)
from on_cloud.notion_api import Notion

##@@ Custom Modules
##------------------------------------------------------------

# sys.path.append(os.path.join(os.path.dirname(__file__), "../api_ebest"))



#@@@ Declaration AREA
##============================================================

##@@ Static Literals / Variables
##------------------------------------------------------------
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
plantuml_to_b64 = bytes.maketrans(plantuml_alphabet.encode('utf-8'), base64_alphabet.encode('utf-8'))

##@@ Dynamic Literals / Variables
##------------------------------------------------------------


##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------


##@@ Public Functions
##------------------------------------------------------------
def plantuml_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')


def plantuml_decode(plantuml_url):
    """decode plantuml encoded url back to plantuml text"""
    data = base64.b64decode(plantuml_url.translate(plantuml_to_b64).encode("utf-8"))
    dec = zlib.decompressobj()  # without check the crc.
    header = b'x\x9c'
    return dec.decompress(header + data).decode("utf-8")



##@@@ Execution AREA
##============================================================
if __name__ == "__main__":
    pass
    notion = Notion()
    page_id = "0bd7f86e934345d2963ef9ef5a495817"

    # url = "SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="

    # print(plantuml_decode(url))
    # print(plantuml_encode(plantuml_decode(url)))

    children = [
        {
            "type": "toggle",
            "toggle": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "",
                    }
                }],
                "color": "default",
                "children":[
                    {
                        'type': 'code',
                        'code': {
                            'rich_text': [{
                                'type': 'text', 
                                'text': {
                                    'content': 'Bob ---> Alice', 
                                }, 
                            }], 
                            # 'language': 'mermaid'
                        }
                    },
                    # {
                    #     "type": "code",
                    #     "code": {
                    #         "rich_text": [{
                    #             "type": "text",
                    #             "text": {
                    #                 "content": "test code block"
                    #             }
                    #         }],
                    #         # "language": "mermaid"
                    #     }
                    # },
                    {
                        "type": "embed",
                        "embed": {
                            "url": "https://kroki.io/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="
                        }
                    }
                    # {
                    #     "type": "image",
                    #     "image": {
                    #         "type": "external",
                    #         "external": {
                    #             "url": "http://www.plantuml.com/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700==.svg"
                    #         }
                    #     }
                    # }
                    # {
                    #     "type": "paragraph",
                    #     "paragraph": {
                    #         "rich_text": [{
                    #         "type": "text",
                    #         "text": {
                    #             "content": "Lacinato kale",
                    #         }
                    #         }],
                    #         "color": "default",
                    #         "children":[]
                    #     }
                    # }
                    # {
                    #     "type": "image",
                    #     "image": {
                    #         "type": "external",
                    #         "external": {
                    #             "url": "http://www.plantuml.com/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="
                    #         }
                    #     }
                    # }
                    # {
                    # "type": "image",
                    # "image": {
                    #     'caption': [], 
                    #     'type': 'external', 
                    #     'external': {
                    #         'url': 'http://www.plantuml.com/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700=='
                    #     }
                    # }
                    # }
                ]
            }
        },
        # {
        #     "type": "image",
        #     "image": {
        #         "type": "external",
        #         "external": {
        #             "url": "https://weaversmind.speedgabia.com/edu/img/220308/cnt_01.png"
        #         }
        #     }
        # }
        # {
        #     "type": "image",
        #     "image": {
        #         "type": "external",
        #         "external": {
        #             "url": "http://www.plantuml.com/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="
        #         }
        #     }
        # }
    ]

# 'type': 'image', 'image': {'caption': [], 'type': 'external', 'external': {'url': 'http://www.plantuml.com/plantuml/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700=='}

    obj_id = "7e656cfeb4864d958a5ff0ab1439aedc"
    # "1a3d6d74297848009f821150557d6a7e"
    # ad631c80d2df4535b36372b2ab47a0a1
    # obj_id = "ad631c80d2df4535b36372b2ab47a0a1"
    notion._append_block(obj_id="0bd7f86e934345d2963ef9ef5a495817", children=children)
    # r = notion._children_block(obj_id="baf1cac744cc4d0e889ab64bb9f7c946")
    # # r = notion._retrieve_block(obj_id=obj_id)
    # print(r)

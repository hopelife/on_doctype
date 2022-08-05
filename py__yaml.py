# -*- coding=utf-8 -*-
"""
Functions: 
    - notion(dict) to py(literal)


Plot:
    - notion code block -> yml(json) -> python literal -> insert to python file

Usages: 
    - 

Requirements:
    # - pip install ruamel.yaml

References:
    - 

Cautions:
    - 

Created:
    - by:
    - started:  
    - updated: 
     
"""

##@@@ Import AREA
##============================================================

# ##@@ Built-In Modules
# ##------------------------------------------------------------
import sys, os
import re
import copy
import json  # TODO: Notion 테스트용, 테스트후 삭제
import time  # TODO: Notion 테스트용, 테스트후 삭제

##@@ Installed Modules
##------------------------------------------------------------
import ruamel.yaml
# from on_builtin.util_data import (_write_file, _read_file, _get_value_nested, _set_value_nested, _get_path_nested, _get_path_nested_by_key, _insert_join)


##@@ Custom Modules
##------------------------------------------------------------


##@@@ Declaration AREA
##============================================================

##@@ Static Literals / Variables
##------------------------------------------------------------


##@@ Dynamic Literals / Variables
##------------------------------------------------------------


##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------

def _from_yaml(yaml_str):
    """
    """
    yaml = ruamel.yaml.YAML()
    string_stream = StringIO()
    yaml.dump(yaml_data, string_stream)
    source_code = string_stream.getvalue()
    string_stream.close()
    return source_code


def _to_yaml(yaml_str, indent=2):
    """
    """
    yaml_str = yaml_str.replace("\t", " "*indent)
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=4, sequence=4, offset=2)
    yaml.preserve_quotes = True
    return yaml.load(yaml_str)


##@@@ Public Function
##============================================================


##@@@ Execution AREA
##============================================================
if __name__ == "__main__":
    pass
    import sys
    from io import StringIO

    INDENTATION = 2
    yaml_str = """  
        "Shopping List": {  
            "eggs": {  
                "type": "free range",  
                "brand": "Mr Tweedy",  
                "amount": 12  
            },  
            "milk": {  
                "type": "pasteurised",  
                "litres": 1.5,  
                "brands": [  
                    "FarmFresh",  
                    "FarmHouse gold",  
                    "Daisy The Cow"  
                ]  
            }  
        }  
    """

    # yaml = ruamel.yaml.YAML()
    # shopping_list = yaml.load(yaml_str)  # Show object type 
    # # shopping_list = yaml.load(yaml.dump(shopping_list))  # Show object type 
    # yaml.indent(mapping=4, sequence=4, offset=2)
    # yaml.preserve_quotes = True 
    # # print(type(shopping_list))

    # shopping_list.yaml_set_start_comment("Shopping Lists for date: 23 Oct 2021")

    # # yaml = ruamel.yaml.YAML()
    # string_stream = StringIO()
    # yaml.dump(shopping_list, string_stream)
    # source_code = string_stream.getvalue()
    # string_stream.close()

    # print(source_code)

    d = {
        "Shopping List": {  
            "eggs": {  
                "type": "free range",  
                "brand": "Mr Tweedy",  
                "amount": 12  
            },  
            "milk": {  
                "type": "pasteurised",  
                "litres": 1.5,  
                "brands": [  
                    "FarmFresh",  
                    "FarmHouse gold",  
                    "Daisy The Cow"  
                ]  
            }  
        }  
    }  


    yaml = ruamel.yaml.YAML()
    # d = dict(a=dict(b=2),c=[3, 4])
    # yaml = YAML()
    yaml.dump(d, sys.stdout)
    # print('0123456789')
    # yaml = YAML()
    # yaml.indent(mapping=4, sequence=6, offset=3)
    # yaml.dump(d, sys.stdout)
    # print('0123456789')
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
from on_builtin.util_data import (_write_file, _read_file, _get_value_nested, _set_value_nested, _get_path_nested, _get_path_nested_by_key, _insert_join)


##@@ Custom Modules
##------------------------------------------------------------
from on_cloud.notion_api import Notion


##@@@ Declaration AREA
##============================================================

##@@ Static Literals / Variables
##------------------------------------------------------------


##@@ Dynamic Literals / Variables
##------------------------------------------------------------
notion = Notion()


##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------
def _extract_codes(blocks):
    """blocks에서 code block 추출
    TODO: block['id']
    """
    codes = {}
    for block in blocks:
        if block['type'] == 'code':
            language = block['code']['language']
            _code = {}
            _code['id'] = block['id'].replace("-", "")
            _code['content'] = block['code']['rich_text'][0]['text']['content']
            if language in codes:
                codes[language] += _code
            else:
                codes[language] = [_code]
    return codes


def _yaml_data_to_string(yaml_data):
    """
    """
    yaml = ruamel.yaml.YAML()
    string_stream = StringIO()
    yaml.dump(yaml_data, string_stream)
    source_code = string_stream.getvalue()
    string_stream.close()
    return source_code


def _string_to_yaml_data(yaml_str, indent=2):
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
    # page notion_2_py: 0bd7f86e934345d2963ef9ef5a495817
    blocks = notion._children_block(obj_id="0bd7f86e934345d2963ef9ef5a495817")

    codes = _extract_codes(blocks)
    yaml_strs = codes["yaml"]
    print(f"{yaml_strs=}")

    import sys
    from io import StringIO

    yaml_str = yaml_strs[0]['content']
    data = _string_to_yaml_data(yaml_str, indent=2)
    # yaml = ruamel.yaml.YAML()
    # yaml.indent(mapping=4, sequence=4, offset=2)
    # yaml.preserve_quotes = True
    # data = yaml.load(yaml_str)
    # print(f"{data=}")
    # params['ParentTest']['test']['new_key'] = 'new value'
    # params['ParentTest']['test'].yaml_add_eol_comment('some comment', key='new_key', column=40) # column is optional
    # yaml.dump(data, sys.stdout)



    # string_stream = StringIO()
    # yaml.dump(data, string_stream)
    # source_code = string_stream.getvalue()
    # string_stream.close()
    # print(f"{source_code=}")
    print(f"{_yaml_data_to_string(data)=}")
    # with open('my_file_new.yaml', 'wb') as f:
    #     yaml.dump(data, f)
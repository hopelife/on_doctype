# -*- coding=utf-8 -*-
'''
[sats]::[C:\Dev\on_document\test.py]
Functions:
    - 
    - 

Todos:
    - 

Usages:
    - 

Requirements:
    - 

Notes:
    - 

Created:
    - by: monblue@snu.ac.kr
    - started: 2022.04.15 10:43
    - updated: 2022.04.15 10:48


'''

##@@@ Import AREA
##============================================================

##@@ Built-In Modules
##------------------------------------------------------------
import os, sys

##@@ Installed Modules
##------------------------------------------------------------
import json

##@@ Custom Modules
##------------------------------------------------------------
if not __package__:
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../on_cloud/on_cloud"))
    from google_sheets import GoogleSheets
    from notion_api import Notion, check_updated_data, notion_strip_data_keys
    # from notion__google import NotionGoogle
else:
    from on_cloud.google_sheets import GoogleSheets
    from on_cloud.notion_api import Notion, check_updated_data, notion_strip_data_keys
    # from on_cloud.notion__google import NotionGoogle
from on_builtin.util_data import _write_file

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


##@@ Public Functions
##------------------------------------------------------------


##@@@ Execution AREA
##============================================================

if __name__ == '__main__':
    # https://developers.notion.com/changelog/column-list-and-column-support
    obj_id = "a79ab625f1424dc5993804240f5147b2"  ## "type": "column_list"
    # obj_id = "dbdab0b935624ce7958d810d053c0099"  ## "type": "column",
    # 3836630c6f0c4b68bfb77eaa6230b45f / 288039a1414845eeb0ef524fe05e811a
    # obj_id = "3836630c6f0c4b68bfb77eaa6230b45f"  ## 
    obj_id = "8b87ead7d1764fe7b0f744403c94b2a1"
    notion = Notion()
    # data = notion._children_block(obj_id=obj_id)
    data = notion._retrieve_block(obj_id=obj_id)
    _write_file(data, "../_data/children_block4_.json")
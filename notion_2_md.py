# -*- coding=utf-8 -*-
"""
Functions: 
    - notion(dict) to markdown(str)
    - TODO: callout / todo / image(file 타입)
    - image: https://www.notion.so/monwork/d063e15dbea24602a31cb1c5044a36de
    -> 페이지 ![title](location)
    ![KIOM_C004_3_0004.jpg](New%20Page%20d063e/KIOM_C004_3_0004.jpg) 

    ![image caption1](https://images.unsplash.com/photo-1511300636408-a63a89df3482?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb)


Plot:
    - notion(dicts) -> parse outer dict(has_children: fetch object) -> parse inner dict -> markdown(str)

Usages: 
    - 

Requirements:
    # - pip install regex

References:
    - https://github.com/echo724/notion2md

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

DEPTH_SEP = "-"
DEPTH_END = ". "
DEPTH_INDENT = "  "

block_map = dict(
    _default = ("", "\n", ["rich_text"], {}, 1),  # start, end, contents (key, ), parse_text
    code = ("```{language}\n", "\n```\n", ["content"], ["language"], 0),
    quote = ("> ", "\n", ["content"], ["_leading"], 0),  # children 계층구조
    equation = ("$$\n", "\n$$\n", ["expression"], [], 0),  
    # bulleted_list_item = ("  ", "\n", ["content"], [], 1),  # children 계층구조
    # numbered_list_item = ("  ", "\n", ["content"], [], 1),  # children 계층구조
)


# inline_map = dict(
#     _default = ("", "\n", ["rich_text"], {}, 1),  # start, end, contents (key, ), parse_text
#     # code = ("```{language}\n", "\n```\n", ["content"], ["language"], 0),
#     # link = ("$$", "$$", ["expression"], [], 0),  
#     # equation = ("$$", "$$", ["expression"], [], 0),  
#     # bulleted_list_item = ("  ", "\n", ["content"], [], 1),  # children 계층구조
#     # numbered_list_item = ("  ", "\n", ["content"], [], 1),  # children 계층구조
# )
# mention > page
# mention > date
# mention > user
# equation > equation > expression


font = dict(
    bold = "**",
    italic = "*",
    strikethrough = "~",
    underline = "_",
    code = "`"
)

##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------

def _hierarchical_numbers(hierarchies, depth):
    """계층(depth) 태그(넘버링) numbered_list_item
    [[1], [1, 1], [1, 2], [1, 2, 1], ...]
    """
    if not hierarchies:
        return [[1]]

    for hierarchy in hierarchies[::-1]:
        _depth = len(hierarchy) - 1

        if depth == _depth + 1:  # NOTE: parent
            new = hierarchy.copy()
            new.append(1)
            hierarchies.append(new)
            break
        elif depth == _depth:  # NOTE: sibling
            new = hierarchy.copy()
            new[-1] = hierarchy[-1] + 1
            hierarchies.append(new)
            break

    return hierarchies


def _leading_str(type, hierachy=[], attr={}):
    """
    계층형 children을 가지는 경우의 leading 문자열
    - bulleted_list_item: '+', '-', '*'
    - numbered_list_item: 
    - to_do: 
    TODO: 변수 -> 설정 상수literal로 
    """
    numbering_types = ["numbered_list_item"]
    if not hierachy:
        return ""

    indent = DEPTH_INDENT*(len(hierachy) - 1)
    if type in numbering_types:
        # print(f"{hierachy=}")
        leading_str = DEPTH_SEP.join([str(n) for n in hierachy])
        return indent + leading_str + DEPTH_END
    else:
        return indent


##@@ Inline Functions
##------------------------------------------------------------

def _text_to_md(inline):
    """
    rich_text/caption/cells 내의 inline -> markdown
    """
    content = inline['text'].get('content', "")
    # link = inline['text'].get('link', None)
    href = inline.get('href', None)
    _annotations = inline.get('annotations', {})
    annotations = [font for font, v in _annotations.items() if v and v != 'default']
    plain_text = inline.get('plain_text', None)

    for annotation in annotations:
        if annotation != 'color':
            content = f"{font[annotation]}{content}{font[annotation]}"

    if href:
        content = f"[{content}]({href})"

# color = rich_texts['color']  ## 전체 글자색

    return content


def _equation_to_md(inline):
    """인라인 수식
    """
    return f"${inline['equation']['expression']}$"
    # return f"$$ {inline['equation']['expression']} $$"


def _mention_to_md(inline):
    """mention
    subtype: 'date' / 'page' / ...
    """
    # print(f"mention {inline}")
    return inline['plain_text'] if not inline['href'] else f"[{inline['plain_text']}]({inline['href']})"

# mention {'type': 'mention', 'mention': {'type': 'user', 'user': {'object': 'user', 'id': '1a3d6d74-2978-4800-9f82-1150557d6a7e', 'name': 'Moon. J. Sam', 'avatar_url': 'https://lh3.googleusercontent.com/a/AATXAJw4-RSw8cuB6tZriYfFAOTg8qlBtgJ8E4ZrRckx=s100', 'type': 'person', 'person': {'email': 'monblue@snu.ac.kr'}}}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '@Moon. J. Sam', 'href': None}
# mention {'type': 'mention', 'mention': {'type': 'page', 'page': {'id': 'e9557c42-8bac-4da3-b16e-11c152be6216'}}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Untitled', 'href': 'https://www.notion.so/e9557c428bac4da3b16e11c152be6216'}


def _inlines_to_md(inlines):
    """
    """
    md = ""
    for inline in inlines:
        type = inline.get('type', None)
        if type == 'text':
            md += _text_to_md(inline)
        elif type == 'equation':
            md += _equation_to_md(inline)
        elif type == 'mention':
            md += _mention_to_md(inline)

    return md


##@@ Block Functions
##------------------------------------------------------------

def _block_to_md(block, hierachy=[]):
    type = block.get("type", None)
    # print(f"{type=}")
    _block_map = block_map.get(type, block_map['_default'])
    bgn_str = _block_map[0]
    end_str = _block_map[1]
    parse_text = _block_map[4]
    text_keys = _block_map[2] # content_keys
    attr_keys = _block_map[3]

    leading_str = _leading_str(type, hierachy)

    _text_keys = {key: _get_path_nested_by_key(key, block) for key in text_keys}
    _attr_keys = {key: _get_path_nested_by_key(key, block) for key in attr_keys}

    attrs = {key: _get_value_nested(path, block) for key, path in _attr_keys.items() if path}

    md = ""
    if parse_text:  # 'annotations' parsing 필요
        for _text_key, path in _text_keys.items():
            if not path:
                continue
            rich_texts = _get_value_nested(path, block)
            md += _inlines_to_md(rich_texts)

        md = f"{bgn_str}{md}{end_str}"
        # print(f"{md=}")
        for key, val in attrs.items():
                md = md.replace(f"{{{key}}}", val)

    else:  # NOTE: text parsing 안함, codeblock 등
        for _text_key, path in _text_keys.items():
            if not path:
                continue
            md = f"{bgn_str}{_get_value_nested(path,block)}{end_str}"
            for key, val in attrs.items():
                md = md.replace(f"{{{key}}}", val)

    # print(f"'{leading_str}{md.strip()}'")
    return f"{leading_str}{md.strip()}" + "\n"


def _serialize_nested_block(block, depth=0, list_items=[]):
    """
    """
    pops = ['object', 'created_time', 'created_by', 'last_edited_time', 'archived', 'color']
    has_children = block['has_children']
    type = block['type']
    id = block['id']

    list_items.append((id, depth))

    if not has_children:
        ## TODO: 이전 yield 덮어쓰기
        yield (depth, block, list_items)
    else:
        # depth += 1
        for child in notion._children_block(obj_id=block['id']):
            yield (depth, block, list_items)
            yield from _serialize_nested_block(child, depth+1, list_items)


##@@ Special Block
##------------------------------------------------------------

def _image_to_md(block):
    """image block 처리
    """
    caption = _inlines_to_md(block['image']['caption'])
    url = block['image'][block['image']['type']]['url']
    return f"![{caption}]({url})" + "\n"


def _table_to_md(block):
    """table block 처리
    """
    children = notion._children_block(obj_id=block['id'])
    # _write_file(children, "./New_Page_table_children.json")
    cols = block['table']['table_width']
    has_header = block['table']['has_column_header']

    delimiter = ""
    if has_header:
        units = ["|---" for _ in range(cols)]
        delimiter = "".join(units) + "|\n"

    rows = []
    for child in children:
        row = "| " + " | ".join([_inlines_to_md(rich_texts) for rich_texts in child['table_row']['cells']]) + " |\n"
        rows.append(row)

    return rows[0] + delimiter + "".join(rows[1:])


##@@ postprocess Functions
##------------------------------------------------------------
def _postprocess(md):
    """markdown 사후(convert 후) 처리
    """
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md


##@@@ Public Function
##============================================================

def page_to_md(page):
    md = ""
    for block in page:
        type = block.get("type", None)
        has_children = block.get("has_children", None)
        if type == 'table':
            md += _table_to_md(block) + "\n"
            continue
        if type == 'image':
            md += _image_to_md(block)
            continue
        # image: block={'object': 'block', 'id': '4ab5fd90-f8c4-4959-a194-91c060455574', 'created_time': '2022-04-03T11:31:00.000Z', 'last_edited_time': '2022-04-07T09:49:00.000Z', 'created_by': {'object': 'user', 'id': '1a3d6d74-2978-4800-9f82-1150557d6a7e'}, 'last_edited_by': {'object': 'user', 'id': '1a3d6d74-2978-4800-9f82-1150557d6a7e'}, 'has_children': False, 'archived': False, 'type': 'image', 'image': {'caption': [{'type': 'text', 'text': {'content': 'image caption1', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'image caption1', 'href': None}], 'type': 'external', 'external': {'url': 'https://images.unsplash.com/photo-1511300636408-a63a89df3482?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb'}}}
        if has_children:
            hierarchies = []
            # md = ""
            for depth, block, list_items in _serialize_nested_block(block, depth=0):
                id = block['id']
                if id not in [_id for (_id, _depth) in list_items[:-1]]:  # NOTE: 중복되지 않은 block
                    hierarchies = [] if not hierarchies else hierarchies
                    hierarchies = _hierarchical_numbers(hierarchies, depth)
                    md += _block_to_md(block, hierachy=hierarchies[-1])
            md += "\n"
        else:
            md += _block_to_md(block) + "\n"

    return _postprocess(md)


##@@@ Execution AREA
##============================================================
if __name__ == "__main__":

    # _dicts = notion._children_block(obj_id="c26d28985a7e40c7aa2263528f0bad47")
    # _write_file(_dicts, "./_data/New_Page.json")

    page = _read_file("./_data/New_Page.json", out_type="json")

    md = page_to_md(page)

    print(md)
# -*- coding=utf-8 -*-
"""
Functions: 
    - markdown(str) to notion(dict)
    - 

Plot:
    - document -> lines -> parse block -> parse inline

Usages: 
    -

Requirements:
    # - pip install regex

References:
    - mistletoe
    - regex
        ## NOTE: 정규표현식Regex
        # ?:  is for non capturing group
        # ?=  is for positive look ahead
        # ?!  is for negative look ahead
        # ?<= is for positive look behind
        # ?<! is for negative look behind

        # () capturing group - the regex inside the parenthesis must be matched and the match create a capturing group
        # (?:) non-capturing group - the regex inside the parenthesis must be matched but does not create the capturing group
        # (?=) positive lookahead - asserts that the regex must be matched
        # (?!) negative lookahead - asserts that it is impossible to match the regex


Cautions:
    - heading: 1~3까지 지원됨(heading_1(#), heading_2(##), heading_3(###))
    - depth: 0, 1, 2 단계까지 depth가 지원됨(depth 2에서는 children을 가질 수 있음)
    - TODO: ', ", |, \n, .... -> 오류 발생하지 않도록 다른 문자로 변경 -> converting 후 재변경
    - TODO: numbered list_item 규칙 자동 인식(전역 변수)
    - TODO: todo list_item depth 공백 간격 자동 인식(전역 변수)
    - TODO: table/footnote
    - TODO: font 속성 'color'  @@red@@
    - TODO: BUG: RecursionError: maximum recursion depth exceeded while getting the repr of an object / SOL: children 처리(quote, )

Created:
    - by:
    - started:  
    - updated: 
     
"""

##@@@ Import AREA
##============================================================

# ##@@ Built-In Modules
# ##------------------------------------------------------------
import re
import copy

##@@ Installed Modules
##------------------------------------------------------------
# import regex

##@@ Custom Modules
##------------------------------------------------------------


##@@@ Declaration AREA
##============================================================

##@@ Static Literals / Variables
##------------------------------------------------------------


##@@ Dynamic Literals / Variables
##------------------------------------------------------------
parsed_lines = []
PATH_SEP = ':'
COUNT_SEP = '-'
INLINE_START = "_{{"
INLINE_END = "}}_"
_DEPTH_INDENT = "  "

_ANNOTATIONS = {  # NOTE: inline object의 구성요소
    "bold": False,
    "italic": False,
    "strikethrough": False,
    "underline": False,
    "code": False,
    "color": "default"
}

# map_annotations = {
#     "strong": "bold",
#     "emphasis": "italic",
#     "strikethrough": "strikethrough",
#     "underline": "underline",
#     "inlinecode": "code"
# }


##@@ Block Configurations
##------------------------------------------------------------
block_settings = dict(  # (parse_text, multi_line, join_line, breakers)
    # paragraph = (1, 1, 1, ['', '>', '#', r'-{3,}']),
    paragraph = (1, 1, 1, ['']),
    # quote = (1, 1, 0, 1, ['']),
    quote = (1, 1, 1, ['']),
    codeblock = (0, 1, 1, ['```']),
    heading_1 = (1, 0, 0, ['']),
    heading_2 = (1, 0, 0, ['']),
    heading_3 = (1, 0, 0, ['']),
    # list_item = (1, 1, 0, 1, ['']),
    numbered_list_item = (1, 1, 0, ['']),
    bulleted_list_item = (1, 1, 0, ['']),
    to_do = (1, 1, 0, ['']),
    table = (1, 0, 0, ['']),
    table_row = (1, 0, 0, ['']),
    table_delimiter = (0, 0, 0, ['']),
    linebreak = (0, 0, 0, ['']),
)


block_patterns = dict(  # NOTE: 순서대로 check함
    # codeblock = (r"\s*```(.*)", {1: 'language'}),  # (pattern, {group: attr})(r'( {0,12}(?:\d{0,9}[.)]|[+\-*]|\[ *[vVxX]* *\]))\s+(.+)', ('_leading', 'content'))
    codeblock = (r"\s*```(.*)(.*)", ('language', 'content')),  # (pattern, {group: attr})  # TODO: codeblock 이후 paragraph 처리
    quote = (r"\s*((> +){1,9})(.+)", ('_leading', '_last', 'content')),
    heading_1 = (r"\s*(#)\s+(.+?)\s*\1?", ('_level', 'content')),
    heading_2 = (r"\s*(##)\s+(.+?)\s*\1?", ('_level', 'content')),
    heading_3 = (r"\s*(#{3,9})\s+(.+?)\s*\1?", ('_level', 'content')),
    # list_item = (r'( {0,12}(?:\d{0,9}[.)]|[+\-*]|\[ *[vVxX]* *\]))\s+(.+)', ('_leading', 'content')),
    bulleted_list_item = (r"( {0,12}[+\-*]) +(.+)", ('_leading', 'content')),
    numbered_list_item = (r"( {0,12}[\d\.\-]+)\s+(.+)", ('_leading', 'content')),  # (r' {0,3}(?:\d{0,9}[.)]|[+\-*]|\[ *[xX]* *\])(?:[ \t]*$|[ \t]+)')
    # numbered_list_item = (r"( {0,12}\d{1,3}[.)])\s+(.+)", ('_leading', 'content')),  # (r' {0,3}(?:\d{0,9}[.)]|[+\-*]|\[ *[xX]* *\])(?:[ \t]*$|[ \t]+)')
    to_do = (r"( {0,12}(\[ *[xX]* *\]))\s+(.+)", ('_leading', 'checked', 'content')),
    # # table = (r"", ('_level', 'content')),  # TODO
    table_row = (r"(?:\|\s+[^:\-](.+)\|)", ('content',)),   # TODO
    table_delimiter = (r"(\|\s*:*?[-]{2,}:\s)+\|", ('content',)),   # TODO r"(\|\s*:*?[-]{2,}:\s)+\|"       r"((?:\|:?[-]+:?)+\|)"      |* *(\-{2,10} *|)+ *|*
    # image = (r"\s*!\[(.+)\]\((.+)\)(.*)", ('alt', 'href', '_content')),  # TODO: _content가 필요한지
    # user1 = (r"\s*'''(.*)", ('class',)),
    # paragraph = ()  # default block
)


block_objects = dict(
    _default = {
        "type": "{type}",
        "{type}": {
            "rich_text": "{content}",
            "color": "default",
            "children": []
        }
    },
    linebreak = {
        "type": "linebreak",
        "linebreak": {

        }
    },
    codeblock = {
        "type": "code",
        "code": {
            "rich_text": "{content}",
            "language": "{language}"
        }
    },
    to_do = {
        "type": "to_do",
        "to_do": {
            "rich_text": [{
            "type": "text",
            "text": {
                "content": "{content}",
                "link": None
            }
            }],
            "checked": "{checked}",
            "color": "default",
            "children":[]
        }
    },
    table = {
        "type": "table",
        "table": {
            "table_width": 3,
            "has_column_header": False,
            "has_row_header": False,
            "children": []
        }
    },
    table_row = {
        "type": "table_row",
        "table_row": {
            "cells": []
        }
    },
    table_cell = [
        {
        "type": "text",
        "text": {
            "content": "{content}",
            "link": "{href}"
        },
        "annotations": _ANNOTATIONS,
        "plain_text": "{content}",
        "href": "{href}"
        }
    ],
    # paragraph = (1, 1, 1, 1, ['', '>', '#', r'-{3,}']),
    # paragraph = {
    #     "type": "paragraph",
    #     "paragraph": {
    #         "rich_text": [{
    #             "type": "text",
    #             "text": {
    #                 "content": "{content}",
    #                 "link": "{link}"
    #             }
    #         }],
    #         "color": "default",
    #         "children":[]
    #     }
    # },
    # quote = {
    #     "type": "quote",
    #     "quote": {
    #     "rich_text": [{
    #         "type": "text",
    #         "text": {
    #             "content": "{content}",
    #         },
    #     }],
    #     "color": "default"
    #     }
    # },
)


##@@ Block Configurations
##------------------------------------------------------------

inline_patterns = dict(  # NOTE: 순서대로 check함
    link = (r"\[(.+)\]\((.+)\)", ('name', 'href')),  # (pattern, {group: attr})
    equation = (r"(\${1,2})([^$]+?)\1", ('_tag', 'content')),
    italic = (r'(?<!\*)\*([^*]{1,})?\*(?!\*)', ('content',)),  #  (?<!\*)\*[^*]+?\*(?!\*)     '\*(?![*\s])(?:[^*]*[^*\s])?\*'  
    # italic = (r'[^*]\*([^*]+)?\*', ('content',)),  #  (?<!\*)\*[^*]+?\*(?!\*)     '\*(?![*\s])(?:[^*]*[^*\s])?\*'  
    bold = (r'\*\*(.+)?\*\*', ('content',)),
    code = (r'`(.+)?`', ('content',)),
    strikethrough = (r'~(.+)?~', ('content',)),  # TODO: ~ 2개 있는 경우도 되도록
    underline = (r'_(.+)?_', ('content',)),  # TODO: _ 2개 있는 경우도 되도록
)


inline_objects = dict(
    _default = {
        "type": "text",
        "text": {
            "content": "{content}",
            # "link": "{link}"
        },
        "annotations": _ANNOTATIONS,
        # "plain_text": None,  # NOTE: 없어도 문제 없음, 하지만 값이 None이면 content가 반영안됨
        # "href": "{href}"
    },
    equation = {
        "type": "equation",
        "equation": {
            "expression": "{content}"
        },
        "annotations": _ANNOTATIONS,
        # "plain_text": "content",
        # "href": None
    },
    link = {
        "type": "text",
        "text": {
            "content": "{name}",
            "link": {
                "url": "{href}"
            }
        },
        "annotations": _ANNOTATIONS,
        # "plain_text": " google",
        "href": "{href}"
    },
    # cell = {
    #     "type": "text",
    #     "text": {
    #         "content": "{content}"
    #     },
    #     "plain_text": "{content}"
    # },
    metnion_date = {  # mention 하위 type
        "type": "date",
        "date": {
            "start": "{start}",
            "end": "{end}",
            "time_zone": "{time_zone}"
        }
    }
    # image = {
    #     "type": "paragraph",
    #     "paragraph": {
    #         "rich_text": [{
    #             "type": "text",
    #             "text": {
    #                 "content": "{content}",
    #                 "link": "{link}"
    #             }
    #         }],
    #         "color": "default",
    #         "children":[]
    #     }
    # },

)



##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------
def _get_value_nested(path, nested):
    """path (key0, key1, key2, ...) -> nested[key1][key2][key3]
    """
    for i, key in enumerate(path):
        if i == len(path) -1: return nested[key]
        else: return _get_value_nested(path[i+1:], nested[key])


def _set_value_nested(value, path, nested):
    for i, key in enumerate(path):
        if i == len(path) -1:
            nested[key] = value
            return nested[key]
        else: 
            return _set_value_nested(value, path[i+1:], nested[key])


def _get_path_nested(value, nested, prepath=()):
    """
    val값을 가지는 path
    """
    for k, v in nested.items():
        path = prepath + (k,)
        if v == value: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
        # elif type(v) == dict: # v is a dict
            p = _get_path_nested(value, v, path) # recursive call
            if p is not None:
                return p


def _get_path_nested_by_key(key, nested, prepath=()):
    """
    하위 key값을 가지는 path
    """
    for k, v in nested.items():
        path = prepath + (k,)
        if k == key: # found key
            return path
        elif hasattr(v, 'items'): # v is a dict
        # elif type(v) == dict: # v is a dict
            p = _get_path_nested_by_key(key, v, path) # recursive call
            if p is not None:
                return p

##@@ Block Functions
##------------------------------------------------------------

def _get_depth(attr, type):
    """
    children을 가지는 block의 depth를 출력: 0: depth 없음, root / 1: 1차 하위 depth
    NOTE: depth는 0, 1, 2만 지원
    """
    if '_leading' not in attr:
        return 0
    elif type == 'quote':
        depth = attr['_leading'].count('>') - 1  # depth = 0 부터 시작
    elif type == 'bulleted_list_item':
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _DEPTH_INDENT).count(_DEPTH_INDENT)  # TODO: 공백 들여쓰기 자동 인식(첫번째 depth1의 indent로 _DEPTH_INDENT 변경)
    elif type == 'to_do':
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _DEPTH_INDENT).count(_DEPTH_INDENT)  # TODO: 공백 들여쓰기 자동 인식(첫번째 depth1의 indent로 _DEPTH_INDENT 변경)
    elif type == 'numbered_list_item':  # 1. > a. > i.
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _DEPTH_INDENT).count(_DEPTH_INDENT)
    # elif type == 'paragraph':
    #     pass

    return depth if depth < 3 else 2


def _set_attr(attr, type):
    """attr에서 key가 '_'로 시작하는 값 제거 ex) _leading, _level 등
    """
    # if type == 'list_item':  # list_item 이면 subtype 지정
    #     attr['subtype'] = 'bulleted' if attr['_leading'].replace(" ", "") in ['+', '-', '*'] else 'todo' if '[' in attr['_leading'] else 'numbered'
    if type == 'to_do':  # list_item 이면 subtype 지정
        attr['checked'] = 'False' if '[]' in attr['checked'].replace(" ", "") else 'True'
        # attr['checked'] = 'False' if '[]' in attr['checked'].replace(" ", "") else 'True'
    # if "table" in type:  # table과 관련된 block
    #     attr['checked'] = 
    for key in [k for k in attr if k.startswith('_')]:
        attr.pop(key)

    return attr


def _type_attr_from_line(line):
    """
    TODO: type, attrs, content
    """
    for type, (pattern, attrs) in block_patterns.items():
        match = re.fullmatch(pattern, line)
        if match:
            if "table" in type:  # NOTE: table과 관련된 block
                return (type, {'content': match.group(0)})
            else:
                return (type, {attr: match.group(i+1) for i, attr in enumerate(attrs)})

    return ('paragraph', {'content': line})  # NOTE: type이 없다면 'paragraph'로 설정


def _object_template(type, block=True):
    """object_template(dict) copy 출력
    inline: block=False
    TODO: {type} 등 key 변경 위치,이름 일반화
    """
    object_templates = block_objects if block else inline_objects

    if type in object_templates:
        object_template = copy.deepcopy(object_templates[type])
    elif block:
        object_template = copy.deepcopy(object_templates['_default'])
        object_template['type'] = type
        object_template[type] = object_template.pop('{type}')
    else:
        object_template = copy.deepcopy(object_templates['_default'])

    return object_template


def _join_inline_content(content, previous_block):
    """inline content 연결(\n + content)
    """
    type = previous_block['type']
    block_template = _object_template(type, block=True)
    path = _get_path_nested("{content}", block_template)

    content = _get_value_nested(path, previous_block).replace(INLINE_START, '').replace(INLINE_END, '') + "\n" + content
    _set_value_nested(f"{INLINE_START}{content}{INLINE_END}", path, previous_block)


def _create_block(type, attr, content_key="content"):
    """
    attr을 적용한 block 생성
    """
    block = _object_template(type, block=True)
    for k, v in attr:
        path = _get_path_nested(f"{{{k}}}", block)
        if k == content_key:
            _set_value_nested(f"{INLINE_START}{attr[k]}{INLINE_END}", path, block)
        else:
            _set_value_nested(v, path, block)

    return block


def _append_root_block(type, attr, parsed_lines, join_line=False):
    """block 생성, parsed_lines에 추가
    """
    ## TODO: attr 치환
    previous_block = parsed_lines[-1]
    if join_line:
        path = _get_path_nested_by_key("children", previous_block)  # children path
        children = _get_value_nested(path, previous_block)

    if not join_line or children:  # 자식이 있으면 join하지 않음
        block = _object_template(type, block=True)
        path = _get_path_nested("{content}", block)
        # _set_value_nested(f"{INLINE_START}{attr['content']}{INLINE_END}", path, block)
        _create_block(type, attr, block, content_key="content")
        parsed_lines.append(block)
    else:  # inline 줄 연결(이음)
        _join_inline_content(attr['content'], previous_block)


def _append_children_block(type, attr, parent_block, join_line=False):
    """이전 block에 자식 블럭으로 추가
    """
    path = _get_path_nested_by_key("children", parent_block)  # children path
    print(f"{parent_block=} {path=}")
    children = _get_value_nested(path, parent_block)

    if not join_line or (not children or _get_value_nested(path, children[-1])):
        child_block = _object_template(type, block=True)  # join하려는 요소(마지막 자식)가 없거나 그 요소에 자식이 있으면 join하지 않음
        path = _get_path_nested("{content}", child_block)  # content 들어갈 path
        # TypeError: 'NoneType' object is not iterable
        _set_value_nested(f"{INLINE_START}{attr['content']}{INLINE_END}", path, child_block)

        children.append(child_block)
    else:
        _join_inline_content(attr['content'], children[-1])


def _append_grandson_block(type, attr, grandparent_block, join_line=False):
    """이전 block에 손자 블럭으로 추가
    """
    path = _get_path_nested_by_key("children", grandparent_block)  # children path
    children = _get_value_nested(path, grandparent_block)
    if children:
        last_child = children[-1]
        last_child_children = _get_value_nested(path, last_child)
    else:
        print("Error: 추가할 children Node가 없습니다.")

    if not join_line or not last_child_children:
        grandson_block = _object_template(type, block=True)
        path = _get_path_nested("{content}", grandson_block)  # content 들어갈 path
        _set_value_nested(f"{INLINE_START}{attr['content']}{INLINE_END}", path, grandson_block)

        _get_value_nested(tuple(list(path)[:-1]), grandson_block).pop('children')  ## NOTE: grandson의 children key 삭제
        last_child_children.append(grandson_block)
    else:
        _join_inline_content(attr['content'], last_child_children[-1])


##@@ Table Functions
##------------------------------------------------------------
def _table_cells_by_content(content):
    """테이블 셀
    """
    if content.startswith('|'): content = content[1:]
    if content.endswith('|'): content = content[:-1]
    return [f"{INLINE_START}{cell.strip()}{INLINE_END}" for cell in content.split('|')]


def _table_block(_type, _attr, type, parsed_lines):
    """테이블 블럭 별도 처리
    """
    if 'table' not in type and _type == 'table_row':  # 첫번째 테이블행(제목 or 제목없는 첫번째 내용)
        cols = _attr['content'][1:-1].count('|') + 1
        table_dict = copy.deepcopy(block_objects['table'])
        table_row_dict = copy.deepcopy(block_objects['table_row'])
        table_dict['table']['table_width'] = cols
        table_row_dict['table_row']['cells'] += _table_cells_by_content(_attr['content'])

        table_dict['table']['children'].append(table_row_dict)
        parsed_lines.append(table_dict)  # NOTE: 테이블 라인

    elif type == 'table' and _type == 'table_delimiter':  # 테이블 구분자
        parsed_lines[-1]['table']['has_column_header'] = True
        # parsed_lines[-2][1]['has_row_header'] = True  # NOTE: table 라인 'has_row_header'값 변경
    elif type == 'table' and _type == 'table_row':  # 일반 행row
        table_row_dict = copy.deepcopy(block_objects['table_row'])
        table_row_dict['table_row']['cells'] += _table_cells_by_content(_attr['content'])
        parsed_lines[-1]['table']['children'].append(table_row_dict)
    elif type == 'table' and 'table' not in _type:  # TODO: 여기 말고 다른 데서 처리?
        pass
        ## TODO: 테이블 구분자가 먼저 나오는 경우 등의 오류
        # print(f"Why are you here??")




def _find_parsed_line(path, parsed_lines):
    """path로 parsed_line 출력
    """
    for line in parsed_lines:
        if path == line[0]:
            return line


def _append_child_dict(_dict, parsed_document, child_line, parsed_lines, appended_line_paths):
    """
    """
    _grandson_paths = child_line[2]
    (type, count, depth) = _type_count_depth(child_line[0])

    print(f"재귀호출 에러? ")
    child_dict = _convert_block(type, child_line[1])
    if not child_line[2]:  # children = []
        appended_line_paths.append(child_line[0])  ## NOTE: 처리된 line으로 표시
        # _dict[type]['children'].append(child_dict)  # child_line[1]: attr child_line[1]: attr
        # parsed_document.append(_dict)
    else:
        for _grandson_path in _grandson_paths:
            appended_line_paths.append(_grandson_path)  ## NOTE: 처리된 line으로 표시
            _append_child_dict(child_dict, parsed_document, _find_parsed_line(_grandson_path, parsed_lines), parsed_lines, appended_line_paths)

    if depth == 2:  # NOTE: quote: 0, 1, 2 단계까지 depth가 지원됨(depth 2에서는 children을 가질 수 있음)
        # print(f"{type=}")
        # print(f"{child_dict[type]=}")
        child_dict[type].pop('children')
        return _dict[type]['children'].append(child_dict)  # child_line[1]: attr child_line[1]: attr

    _dict[type]['children'].append(child_dict)  # child_line[1]: attr child_line[1]: attr

    return appended_line_paths


##@@ Inline Functions
##------------------------------------------------------------
def _convert_inline(type, attr):
    """type에 맞는 block template(dict)에 attr 값을 삽입
    """
    _dict = copy.deepcopy(inline_objects[type]) if type in inline_objects else copy.deepcopy(inline_objects['_default'])
    if type == 'link': print(f"link {_dict}", "+"*100)
    s = str(_dict)
    # print(f"_convert_inline: {s=} {attr=}")
    # if not attr['content']: print(f"NONE attr {type}", "*"*50)
    if not attr: print(f"NONE attr {type}", "*"*50)
    # s = s.replace("{type}", type)
    for k, v in attr.items():
        if v:  # NOTE: AttributeError: 'NoneType' object has no attribute 'replace'
            # print(f"type: {type} {k}: {v}")
            s = s.replace(f"{{{k}}}", v.replace("\n", "\\n"))  ## NOTE: 개행문자로 인한 오류 방지
    # s = re.sub(r"': '\{.+\}'", "': None", s)  ## TODO: BUG: {'type': 'text', 'text': {'content': 'raw0 ', 'link': None} SyntaxError: unexpected EOF while parsing
    return eval(s)


def _find_inline_elements(line):
    """inline 요소 검색
    """
    inlines = []
    for type, (pattern, attr) in inline_patterns.items():
        for match in re.finditer(pattern, line):
            none_marker = False  # None을 
            if not match: break 
            el = {}
            for i, key in enumerate(attr):  ## NOTE: group 내에 None이 있으면 제외
                if not match.group(i+1):
                    # print(f"BREAK")
                    none_marker = True
                    break
                el[key] =  match.group(i+1)
            if not none_marker: inlines.append((match.span(), type, el))  # (position, type, attr)

    return inlines


def _sort_and_convert_inlines(line, inlines):
    """position 순으로 정렬
    line: 원래 문자열
    inlines: 검색된 inline 요소들
    """
    converted = []
    cursor = 0
    # TODO, BUG: italic: {'content': None}
    for ((start, end), type, attr) in sorted(inlines, key = lambda x: x[0][0]):
        # if type == 'italic': start += 1  # NOTE: italic pattern의 첫글자는 '*'가 아닌 문자이므로

        if cursor < start:  # NOTE: 비어있는 부분 rawtext로 채움
            converted.append(_convert_inline('rawtext', dict(content=line[cursor:start])))
            # print(f"rawtext: '{line[cursor:start]}'")
        # if attr.get('content', None):  # NOTE: 검색된 inline 요소 부분 # TODO, BUG: italic: {'content': None}
        _dict = _convert_inline(type, attr)
        if type in _dict['annotations']:  # TODO: type과 annotations이 일치하지 않는 경우
            _dict['annotations'][type] = True
        converted.append(_dict)  # NOTE: 검색된 inline 요소 부분 # TODO, BUG: italic: {'content': None}
        # if attr['content']: converted.append(_convert_inline(type, attr))
        # print(f"{type}: {attr}")
        cursor = end

    ## NOTE: 끝에 남은 부분  
    # rawtext = line[cursor:]
    # print(f"rawtext: '{line[cursor:]}'")
    converted.append(_convert_inline('rawtext', dict(content=line[cursor:]))) # TODO, BUG: italic: {'content': None}
    # print(f"마지막 rawtext: '{rawtext}'")
    return converted


##@@@ Public Function
##============================================================
def document_to_lines(document, repls={}):
    """document -> lines
    TODO: 
    # 공백/개행문자 처리: rstrip(), \n{3,} -> \n\n
    # 특수문자 처리: "', (str <-> dict, json에 문제가 되는 문자)
    # header / table / footnote 표시
    #   - table: table 첫라인 검색: column 개수 / 2번째 라인 검색: header 유무, align / 마지막 라인: row 개수 -> 시작, 끝 표시 (col, row, (align,))
    """
    return document.splitlines()


def parse_block(lines):
    parsed_lines = [block_objects['linebreak']]  ## (path, value, children)

    for line in lines:
        ## NOTE: 이전 라인 path, attr, children
        previous_block = parsed_lines[-1]
        type = previous_block['type']
        (parse_text, multi_line, join_line, breakers) = block_settings[type]
        
        ## NOTE: 현재 라인 type, attr, depth
        (_type, _attr) = _type_attr_from_line(line) 
        _depth = _get_depth(_attr, _type)
        join_line = join_line and _type == type and multi_line
        print(f"{join_line=}")

        ## path 변경(new, child) / value JOIN
        if line.strip() in breakers:  ## 현재 라인이 linebreaker에 해당하면, 블럭 초기화, TODO: 연속으로 null 블럭("linebreak", {'content': ''}, [])이 나오는 것은 없앨 것
            # if type != 'linebreak':  # TODO: 테스트 후 조정
            #     parsed_lines.append(block_objects['linebreak'])
            continue
        else:
            ## NOTE: table 처리, TODO: footnote, ... 처리
            if 'table' in _type:
                _table_block(_type, _attr, type, parsed_lines)
                continue

            if _depth == 0:
                _append_root_block(_type, _attr, parsed_lines, join_line=join_line)
            elif _depth == 1:
                _append_children_block(_type, _attr, previous_block, join_line=join_line)
            elif _depth == 2:
                _append_grandson_block(_type, _attr, previous_block, join_line=join_line)

    return parsed_lines


def parse_inline(blocks):
    for block in blocks:
        # 


def apply_inline(parsed_lines):
    """parsed_lines -> inline 요소 적용
    TODO: parse_text: 0인 type은 적용하지 않음
    """
    converted_lines_str = str(parsed_lines)

    for match in re.finditer(r"[\'\"](rich_text|caption)[\'\"]\s*:\s*[\'\"]([^']+)?[\'\"]", converted_lines_str):
        # print(match.group())
        (org, key, line) = (match.group(0), match.group(1), match.group(2))
        inlines = _find_inline_elements(line)
        content = str(_sort_and_convert_inlines(line, inlines))
        converted_lines_str = converted_lines_str.replace(org, f"'{key}': {content}")
    
    return converted_lines_str.replace("'True'", 'True').replace("'False'", 'False')


def apply_inline_table(parsed_lines):
    """parsed_lines -> inline 요소 적용
    """
    converted_lines_str = str(parsed_lines)

    # for match in re.finditer(r"[\'\"](cells)[\'\"]\s*:\s*\[[\'\"]([^']+)?[\'\"]", converted_lines_str):
    for cell_line in re.findall(r"'{{[^}]+}}'", converted_lines_str):
        line = cell_line[3:-3]
        inlines = _find_inline_elements(line)
        content = str(_sort_and_convert_inlines(line, inlines))
        converted_lines_str = converted_lines_str.replace(cell_line, content)

    return converted_lines_str.replace("'True'", 'True').replace("'False'", 'False')


##@@@ Execution AREA
##============================================================
if __name__ == "__main__":
    pass

    ## NOTE: TEST BLOCK
    document = """"
paragraph *1234* ~strikethrough~ 
paragraph line2

- quote0
  - quote0-0

> quote0-1 [link1](url1) quote mark1 $$E=MC^2$$ text
> > quote0-0-1 **bold** quote mark2
> > > quote0-0-1-0 *italic* -> quote0-0-2
> > quote0-0-1-0  -> quote0-0-2"""

# #     document = """"
# # [] list0
# #   [X] list0-0
# #     [] list0-0-0
# #     [X] list0-0-1
# # """
# #     document = """"
# # 1. list0
# #   1.1. list0-0
# #     1.1.1. list0-0-0
# #     1.1.2. list0-0-1
# # """

# #     document = """| Tables        | Are           | Cool  |
# # | :-------------: | :-------------: | :-----: |
# # |   **col 3** is      |    ~r-l~ *italic*        | $1600 |
# # | col 2 is      | centered      |   ~$12~ |
# # | _zebra stripes_ africa | are neat      |    $1 |
# # """

# #     document = """| Tables        | Are           | Cool  |
# # |   **col 3** is      |    ~r-l~ *italic*        | $1600 |
# # | col 2 is      | centered, 'quote', "double quote"      |   ~$12~ |
# # | _zebra stripes_ africa | are neat      |    $1 |
# # """

#     with open("test1.md", "r", encoding="utf-8") as f:
#         document = f.read()

    # ## NOTE: TEST BLOCK
    lines = document_to_lines(document, repls={})
    # for line in lines:
    #     print(f"'{line}'")
    parsed_lines = parse_block(lines)
    print(parsed_lines)

#     converted_lines = apply_block(parsed_lines)
#     # print(converted_lines)

#     ## NOTE: TEST INLINE
#     r = apply_inline(converted_lines)
#     r = apply_inline_table(r).replace("'{content}'", "''")  # TODO: 특수문자 뒤에 아무것도 없을 때 발생, 함수에서 제거
#     print(r)

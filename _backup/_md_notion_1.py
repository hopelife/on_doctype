# -*- coding=utf-8 -*-
"""
Functions: 
    - markdown(str) to notion(dict)
    - 

Usages: 
    -

Requirements:
    # - pip install regex

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

# ##@@@ Import AREA
# ##============================================================

# ##@@ Built-In Modules
# ##------------------------------------------------------------


# ##@@ Installed Modules
# ##------------------------------------------------------------


# ##@@ Custom Modules
# ##------------------------------------------------------------


# ##@@@ Declaration AREA
# ##============================================================

# ##@@ Static Literals / Variables
# ##------------------------------------------------------------


# ##@@ Dynamic Literals / Variables
# ##------------------------------------------------------------


# ##@@@ Definition AREA
# ##============================================================

# ##@@ Private Functions
# ##------------------------------------------------------------



# ##@@ Public Functions
# ##------------------------------------------------------------



# ##@@@ Execution AREA
# ##============================================================
# if __name__ == "__main__":
#     pass

import re
import copy
# import regex
# content = "Welcome everyone to\rthe world of Geeks\n\nGeeksforGeeks"


parsed_lines = []
PATH_SEP = ':'
COUNT_SEP = '-'
_depth_indent = "  "
# HAS_DEPTHS = ['quote', 'numbered_list_item', 'bulleted_list_item', 'to_do']
# HAS_LEVELS = ['heading']

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


# (path, type, value)
# parsed_lines = [("ROOT", "", "")]

# (path, value)
# parsed_lines = [("ROOT", "")]

# (parse_text, multi_line, join_line, has_children, breakers)
block_settings = dict(
    # paragraph = (1, 1, 1, 1, ['', '>', '#', r'-{3,}']),
    paragraph = (1, 1, 1, 1, ['']),
    # quote = (1, 1, 0, 1, ['']),
    quote = (1, 1, 1, 1, ['']),
    codeblock = (0, 1, 1, 0, ['```']),
    heading_1 = (1, 0, 0, 0, ['']),
    heading_2 = (1, 0, 0, 0, ['']),
    heading_3 = (1, 0, 0, 0, ['']),
    # list_item = (1, 1, 0, 1, ['']),
    numbered_list_item = (1, 1, 0, 1, ['']),
    bulleted_list_item = (1, 1, 0, 1, ['']),
    to_do = (1, 1, 0, 1, ['']),
    table = (1, 0, 0, 1, ['']),
    table_row = (1, 0, 0, 1, ['']),
    table_delimiter = (0, 0, 0, 0, ['']),
    linebreak = (0, 0, 0, 0, ['']),
)

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


# (?<!\*)[^*]+?\*?!\*
# abc *def* **ghi** *jkl* 
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


##@@ Block Functions
##------------------------------------------------------------

def _get_depth(attr, type):
    """
    children을 가지는 block의 depth를 출력: 0: depth 없음, root / 1: 1차 하위 depth
    """
    if '_leading' not in attr:
        return 0
    elif type == 'quote':
        depth = attr['_leading'].count('>') - 1  # depth = 0 부터 시작
    # elif type == 'list_item':
    #     depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)
        # depth = len(re.findall(r"[+\-*]",  attr['_leading'])) - 1  # depth = 0 부터 시작
        # depth = attr['_leading'].count('  ')  # TODO: attr['_leading'] 앞에 있는 공백 문자 개수? 2
    elif type == 'bulleted_list_item':
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)  # TODO: 공백 들여쓰기 자동 인식(첫번째 depth1의 indent로 _depth_indent 변경)
    elif type == 'to_do':
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)  # TODO: 공백 들여쓰기 자동 인식(첫번째 depth1의 indent로 _depth_indent 변경)
    elif type == 'numbered_list_item':  # 1. > a. > i.
        depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)
        # depth = len(re.findall(r"[.\-\)]",  attr['_leading'])) - 1  # TODO: attr['_leading'] 의 구조에 따라? [1. 1.1 1.1.1 / 1. 1-1. / 1-1-1.] [1., 1), 1-1)], [1., a. ]...
        # depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)  # TODO: attr['_leading'] 의 구조에 따라? [1., 1), 1-1)], ...
        # depth = re.split(r'\S', attr['_leading'])[0].replace("\t", _depth_indent).count(_depth_indent)  # TODO: attr['_leading'] 의 구조에 따라? [1., 1), 1-1)], ...

    return depth if depth < 3 else 2


def _type_count_depth(path):
    """path -> type, count
    """
    depth = path.count(PATH_SEP) if path.count(PATH_SEP) < 3 else 2
    # _get_depth(attr, type)
    last = path.rsplit(PATH_SEP, 1)[-1]
    (type, count) = last.rsplit(COUNT_SEP, 1)  # NOTE: (type, count)
    return (type, count, depth)


# def _previous_sibling_path(path, lines):
#     """형제 path
#     """
#     # lines.reverse()
#     for line in reversed(lines):
#         if path.rsplit(PATH_SEP, 1)[-1].rsplit(COUNT_SEP, 1)[0] != line[0].rsplit(PATH_SEP, 1)[-1].rsplit(COUNT_SEP, 1)[0]:  # NOTE: type이 다른 경우, TODO: 확인 필요
#             return None
#         if line[0].count(":") == path.count(":"):
#             return line[0]


def _is_sibling(type, depth, line):
    """(type, depth) 속성을 가지는 라인이 line과 형제인가?
    """
    (_type, _count, _depth) = _type_count_depth(line[0])
    if type == _type and depth == _depth: return True
    return False


def _previous_sibling_path(type, depth, parsed_lines):
    """형제 path
    """
    # lines.reverse()
    # _parsed_lines = copy.deepcopy(parsed_lines)
    for line in reversed(parsed_lines):
        if _is_sibling(type, depth, line):
            return line[0]

    return None


# (type, count, depth) = _type_count_depth(path)

def _set_path(type, depth, parsed_lines):
    """path 설정
    """
    for line in reversed(parsed_lines):
        if _is_sibling(type, depth, line):
            (_path, sn) = line[0].rsplit(COUNT_SEP, 1)  # NOTE: linebreak
            return f"{_path}{COUNT_SEP}{int(sn)+1}"
        elif depth > 0 and _is_sibling(type, depth-1, line):
            return f"{line[0]}{PATH_SEP}{type}{COUNT_SEP}0"
        # parent_path = _parent_path(type, depth, parsed_lines)

    return f"{type}{COUNT_SEP}0"
    # # print(f"type: {type}, depth: {depth}, sibling: {sibling}", "%"*20)
    # if not sibling:
    #     parent_path = _parent_path(type, depth, parsed_lines)
    #     # print("_set_path NOT sibling", f"{parent_path}{PATH_SEP}{type}{COUNT_SEP}0" if parent_path else f"{type}{COUNT_SEP}0")
    #     return f"{parent_path}{PATH_SEP}{type}{COUNT_SEP}0" if parent_path else f"{type}{COUNT_SEP}0"
    # else:
    #     (_path, sn) = (type, -1) if not sibling else sibling.rsplit(COUNT_SEP, 1)  # NOTE: linebreak
    #     print("_set_path WITH sibling", f"{_path}{COUNT_SEP}{int(sn)+1}")
    #     return f"{_path}{COUNT_SEP}{int(sn)+1}"


def _parent_path(type, depth, parsed_lines):  # TODO(X): depth를 path에 표시  quote/1-1:quote/2-1: 
    """부모 path
    """
    return _previous_sibling_path(type, depth-1, parsed_lines)



def _append_children(path, type, depth, parsed_lines):
    """path를 parent의 children에 추가
    """
    parent_path = path.rsplit(PATH_SEP, 1)[0]
    # parent_path = _parent_path(type, depth, parsed_lines)
    parsed_lines.reverse()
    for line in parsed_lines:
        if line[0] == parent_path:
            line[2].append(path)
    parsed_lines.reverse()  # linse 리스트 재역순
    return parsed_lines


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


def _line_type_attr(line):
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



def _convert_block(type, attr):
    """type에 맞는 block template(dict)에 attr 값을 삽입
    """
    ## TODO: table 별도 처리

    # type = f"{attr['subtype']}{type}" if type == "list_item" else type
    # _dict = block_objects[type] if type in block_objects else block_objects['_default']  # BUG RecursionError: maximum recursion depth exceeded while calling a Python object
    print(f"재귀호출 에러? _convert_block")
    _dict = copy.deepcopy(block_objects[type]) if type in block_objects else copy.deepcopy(block_objects['_default'])

    s = str(_dict)
    s = s.replace("{type}", type)
    for k, v in attr.items():
        s = s.replace(f"{{{k}}}", v.replace("\n", "\\n"))  ## NOTE: 개행문자로 인한 오류 방지
    # s = re.sub(r"': '\{.+\}'", "': None", s)  ## NOTE: TODO: content를 변경해버릴 가능성은? code block?
    return eval(s)


def _table_cells_by_content(content):
    """
    """
    if content.startswith('|'): content = content[1:]
    if content.endswith('|'): content = content[:-1]
    return [f"{{{{{cell.strip()}}}}}" for cell in content.split('|')]


# def _table_block(_type, _attr, type, parsed_lines):
#     """테이블 블럭 별도 처리
#     """
#     if 'table' not in type and _type == 'table_row':  # 첫번째 테이블행(제목 or 제목없는 첫번째 내용)
#         cols = _attr['content'][1:-1].count('|') + 1
#         table_path = _set_path('table', 0, parsed_lines)
#         parsed_lines.append((table_path, {'table_width': cols, 'has_column_header': False, 'has_row_header': False}, []))  # NOTE: 테이블 라인
#         parsed_lines.append((f"{table_path}{PATH_SEP}table_row{COUNT_SEP}0", {}, _table_cells_by_content(_attr['content'])))  # NOTE: 테이블 라인
#         # parsed_lines.append((_set_path('table_cell', 0, parsed_lines), {'content': ''}, []))  # NOTE: 테이블 라인
#     elif type == 'table_row' and _type == 'table_delimiter':  # 테이블 구분자
#         parsed_lines[-2][1]['has_row_header'] = True  # NOTE: table 라인 'has_row_header'값 변경
#     elif type == 'table_row' and _type == 'table_row':  # 일반 행row
#         (stem, count) = parsed_lines[-1][0].rsplit(COUNT_SEP, 1)
#         parsed_lines.append((f"{stem}{COUNT_SEP}{int(count) + 1}", {}, _table_cells_by_content(_attr['content'])))  # NOTE: 테이블 라인
#     elif type == 'table_row' and 'table' not in _type:  # TODO: 여기 말고 다른 데서 처리?
#         pass
#         ## TODO: 테이블 구분자가 먼저 나오는 경우 등의 오류


def _table_block(_type, _attr, type, parsed_lines):
    """테이블 블럭 별도 처리
    """
    if 'table' not in type and _type == 'table_row':  # 첫번째 테이블행(제목 or 제목없는 첫번째 내용)
        cols = _attr['content'][1:-1].count('|') + 1

        table_path = _set_path('table', 0, parsed_lines)
        table_dict = copy.deepcopy(block_objects['table'])
        table_row_dict = copy.deepcopy(block_objects['table_row'])
        table_dict['table']['table_width'] = cols
        # table_row_dict['table_row']['cells'].append(_table_cells_by_content(_attr['content']))
        table_row_dict['table_row']['cells'] += _table_cells_by_content(_attr['content'])

        table_dict['table']['children'].append(table_row_dict)
        parsed_lines.append((table_path, table_dict, []))  # NOTE: 테이블 라인

    elif type == 'table' and _type == 'table_delimiter':  # 테이블 구분자
        parsed_lines[-1][1]['table']['has_column_header'] = True
        # parsed_lines[-2][1]['has_row_header'] = True  # NOTE: table 라인 'has_row_header'값 변경
    elif type == 'table' and _type == 'table_row':  # 일반 행row
        table_row_dict = copy.deepcopy(block_objects['table_row'])
        table_row_dict['table_row']['cells'] += _table_cells_by_content(_attr['content'])
        parsed_lines[-1][1]['table']['children'].append(table_row_dict)
        # (stem, count) = parsed_lines[-1][0].rsplit(COUNT_SEP, 1)
        # parsed_lines.append((f"{stem}{COUNT_SEP}{int(count) + 1}", {}, _table_cells_by_content(_attr['content'])))  # NOTE: 테이블 라인
    elif type == 'table' and 'table' not in _type:  # TODO: 여기 말고 다른 데서 처리?
        pass
        ## TODO: 테이블 구분자가 먼저 나오는 경우 등의 오류
        # print(f"Why are you here??")


def _convert_table(type, attr, rows):
    """테이블 처리
    """
    pass


def parse_block(lines):
    # lines = document.splitlines()
    parsed_lines = [("linebreak-0", {'content': ''}, [])]  ## (path, value, children)

    for line in lines:
        ## NOTE: 이전 라인 path, attr, children
        (path, attr, children) = parsed_lines[-1]  
        (type, count, depth) = _type_count_depth(path)
        (parse_text, multi_line, join_line, has_children, breakers) = block_settings[type]
        depth = _get_depth(attr, type)
        
        ## NOTE: 현재 라인 type, attr, depth
        (_type, _attr) = _line_type_attr(line) 
        _depth = _get_depth(_attr, _type)

        ## path 변경(new, child) / value JOIN
        if line.strip() in breakers:  ## 현재 라인이 linebreaker에 해당하면, 블럭 초기화, TODO: 연속으로 null 블럭("linebreak", {'content': ''}, [])이 나오는 것은 없앨 것
            if type != 'linebreak':
                parsed_lines.append((_set_path('linebreak', 0, parsed_lines), {'content': ''}, []))
            continue
        else:
            if _type not in list(block_settings.keys()): continue  ## BUG: 정해지지 않은 type이면 초기화.되돌림, 1줄에 '##'만 있는 경우 KeyError: 'heading' 발생

            ## NOTE: table 처리, TODO: footnote, ... 처리
            if 'table' in _type:
                # print(f"table process {_type}")
                _table_block(_type, _attr, type, parsed_lines)
                continue
            # if 'table' in type or 'table' in _type:
            #     _table_block(_type, _attr, type, parsed_lines)
            #     continue

            if type != 'linebreak' and not parse_text:  # NOTE: codeblock 줄 이음
                attr['content'] = attr.get('content', '')
                attr['content'] += '\n' + _attr['content']
            elif (type == 'linebreak') or (not multi_line) or (type != _type) or (not has_children):  ## 새로운 블럭(루트)인 경우(현재 라인이 linebreak / 이전 라인이 multi_line이 안되는 경우 / 현재 라인과 이전 라인의 type이 다른 경우)
                # print("새로운 블럭(루트)인 경우", "-"*80)
                parsed_lines.append((_set_path(_type, 0, parsed_lines), _set_attr(_attr, _type), []))  # root block(line) 추가
            # elif _depth == depth:  ## 이전 라인과 형제sibling인 경우
            elif join_line:
                attr['content'] += '\n' + _attr['content']
            # else:  # 형제 line 생성
            #     parsed_lines.append((_set_path(_type, _depth, parsed_lines), _set_attr(_attr, _type), []))
            else:  # NOTE: 부모 line에 children 추가
                _path = _set_path(_type, _depth, parsed_lines)
                _append_children(_path, _type, _depth, parsed_lines)  # TODO: 제대로 작동하지는 확인 필요!!!
                parsed_lines.append((_path,  _set_attr(_attr, _type), []))
 
    return parsed_lines


def parse_inline(line):  # inline / block(single_line) heading, paragraph(1 line)
    return line


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


# def _find_inline_elements(line):
#     """inline 요소 검색
#     """
#     inlines = []
#     for type, (pattern, attr) in inline_patterns.items():
#         for match in re.finditer(pattern, line):
#             ## TODO group 내에 None이 있으면 제외
#             if match: inlines.append((match.span(), type, {key: match.group(i+1) for i, key in enumerate(attr) if match.group(i+1)}))  # (position, type, attr)
#             # if match: inlines.append(dict(type=type, pos=match.span(), attr={key: match.group(i+1) for i, key in enumerate(attr)}))
#     return inlines

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

# text_dict = copy.deepcopy(_TEXT_INLINE)
# text_dict['text'] = dict(text_dict['text'], content=content, link=link)
# if name in map_annotations.keys():
#     annotations = copy.deepcopy(_ANNOTATIONS)
#     annotations[map_annotations[name]] = True
#     text_dict['annotations'] = annotations
# map_annotations

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


def apply_block(parsed_lines):
    """parsed_lines -> object(dict) list
    """
    parsed_document = []
    appended_line_paths = []  # NOTE: children으로 등록된 line
    for idx, (path, attr, children) in enumerate(parsed_lines):
        if path in appended_line_paths:  ## 이미 children으로 등록되었으면
            continue

        (type, count, depth) = _type_count_depth(path)

        if type == "table": ## NOTE: table 별도 처리, TODO: _table_block에서 모두 처리
            _dict = attr
        else:
            _dict = _convert_block(type, attr)

            if not children:
                # print(f"without child {type=} {depth=} {_dict=}")
                appended_line_paths.append(path)
            else:  # NOTE: 자식 라인이 있는 경우
                # print(f"WITH children {type=} {depth=}")
                for child_path in children:
                    appended_line_paths.append(child_path)
                    _append_child_dict(_dict, parsed_document, _find_parsed_line(child_path, parsed_lines), parsed_lines, appended_line_paths)
                
        if _dict: parsed_document.append(_dict)  # NOTE: _dict가 linebreak인 경우 None, {} 인 경우 제외
    
    # print(f"{appended_line_paths=}")  # TODO: BUG 목록이 제대로 형성되지 않음: appended_line_paths=['linebreak-0', 'quote-0:quote-0', 'quote-0:quote-0:quote-0', 'quote-0:quote-0:quote-0']

    return parsed_document


def apply_inline(parsed_lines):
    """parsed_lines -> inline 요소 적용
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

# [{'type': 'table', 'table': {'table_width': 3, 'has_column_header': False, 'has_row_header': True, 'children': [{'type': 'table_row', 'table_row': {'cells': ['Tables', 'Are', 'Cool']}}, {'type': 'table_row', 'table_row': {'cells': ['col 3 is'__'r-l'__'$1600'__]}}, {'type': 'table_row', 'table_row': {'cells': ['col 2 is', 'centered', '$12']}}, {'type': 'table_row', 'table_row': {'cells': ['zebra stripes', 'are neat', '$1']}}]}}]

# # [{'type': 'table', 'table': {'table_width': 3, 'has_column_header': False, 'has_row_header': True, 'children': [{'type': 'table_row', 'table_row': {'cells': ['Tables', 'Are', 'Cool']}}, {'type': 'table_row', 'table_row': {'cells': ['col 3 is', 'r-l', '$1600']}}, {'type': 'table_row', 'table_row': {'cells': ['col 2 is', 'centered', '$12']}}, {'type': 'table_row', 'table_row': {'cells': ['zebra stripes', 'are neat', '$1']}}]}}]

##@@@ Execution AREA
##============================================================
if __name__ == "__main__":
    ## NOTE: TEST BLOCK
#     document = """"- quote0
#   - quote0-0
# > > quote0-1 [link1](url1) quote mark1 $$E=MC^2$$ text
# > > > quote0-0-1 **bold** quote mark2
# > > > > quote0-0-1-0 *italic* -> quote0-0-2
# > > quote0-0-1-0  -> quote0-0-2"""
#     document = """"
# - list0
#   + list0-0
#     * list0-0-0
#     * list0-0-1
# """
#     document = """"
# [] list0
#   [X] list0-0
#     [] list0-0-0
#     [X] list0-0-1
# """
#     document = """"
# 1. list0
#   1.1. list0-0
#     1.1.1. list0-0-0
#     1.1.2. list0-0-1
# """

#     document = """| Tables        | Are           | Cool  |
# | :-------------: | :-------------: | :-----: |
# |   **col 3** is      |    ~r-l~ *italic*        | $1600 |
# | col 2 is      | centered      |   ~$12~ |
# | _zebra stripes_ africa | are neat      |    $1 |
# """

#     document = """| Tables        | Are           | Cool  |
# |   **col 3** is      |    ~r-l~ *italic*        | $1600 |
# | col 2 is      | centered, 'quote', "double quote"      |   ~$12~ |
# | _zebra stripes_ africa | are neat      |    $1 |
# """

    with open("test1.md", "r", encoding="utf-8") as f:
        document = f.read()

    # ## NOTE: TEST BLOCK
    lines = document_to_lines(document, repls={})
    # for line in lines:
    #     print(f"'{line}'")
    parsed_lines = parse_block(lines)
    # print(parsed_lines)

    converted_lines = apply_block(parsed_lines)
    # print(converted_lines)

    ## NOTE: TEST INLINE
    r = apply_inline(converted_lines)
    r = apply_inline_table(r).replace("'{content}'", "''")  # TODO: 특수문자 뒤에 아무것도 없을 때 발생, 함수에서 제거
    print(r)

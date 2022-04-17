import re
import copy

content = "Welcome everyone to\rthe world of Geeks\n\nGeeksforGeeks"


buff_lines = []
PATH_SEP = ':'
COUNT_SEP = '-'
# HAS_DEPTHS = ['quote', 'numbered_listitem', 'bulleted_listitem', 'todo_listitem']
# HAS_LEVELS = ['heading']


# (path, type, value)
# buff_lines = [("ROOT", "", "")]

# (path, value)
# buff_lines = [("ROOT", "")]

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
    numbered_listitem = (1, 1, 0, 1, ['']),
    bulleted_listitem = (1, 1, 0, 1, ['']),
    todo_listitem = (1, 1, 0, 1, ['']),
    linebreak = (0, 0, 0, 0, ['']),
)

block_patterns = dict(  # NOTE: 순서대로 check함
    # codeblock = (r"\s*```(.*)", {1: 'language'}),  # (pattern, {group: attr})
    codeblock = (r"\s*```(.*)", ('language',)),  # (pattern, {group: attr})
    quote = (r"\s*((> *){1,9})([^>]+)", ('_leading', '_last', 'content')),
    heading_1 = (r"\s*(#)\s+(.+?)\s*\1?", ('_level', 'content')),
    heading_2 = (r"\s*(##)\s+(.+?)\s*\1?", ('_level', 'content')),
    heading_3 = (r"\s*(#{3,9})\s+(.+?)\s*\1?", ('_level', 'content')),
    heading = (r"\s*(#{1,9})\s*(.*?)\s*\1?", ('_level', 'content')),
    numbered_listitem = (r"", ('_leading', 'content')),
    bulleted_listitem = (r"", ('_leading', 'content')),
    todo_listitem = (r"", ('_leading', 'done', 'content')),
    table = (r"", ('_level', 'content')),  # TODO
    table_row = (r"", ('_level', 'content')),   # TODO
    image = (r"\s*!\[(.+)\]\((.+)\)(.*)", ('alt', 'href', '_content')),  # TODO: _content가 필요한지
    user1 = (r"\s*'''(.*)", ('class',)),
    # paragraph = ()  # default block
)


block_objects = dict(
    _default = {
        "type": "{type}",
        "{type}": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "{content}",
                    "link": "{link}"
                },
            }],
            "color": "default",
            "children":[]
        }
    },
    linebreak = {

    },
    # paragraph = (1, 1, 1, 1, ['', '>', '#', r'-{3,}']),
    paragraph = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "{content}",
                    "link": "{link}"
                }
            }],
            "color": "default",
            "children":[]
        }
    },
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


inline_patterns = dict(  # NOTE: 순서대로 check함
    # codeblock = (r"\s*```(.*)", {1: 'language'}),  # (pattern, {group: attr})
    link = (r"\[(.+)\]\((.+)\)", ('name', 'href')),  # (pattern, {group: attr})
    bold = (r"(\*{2})([^*]+)\1", ('font', 'content')),
    italic = (r"(\*)([^*]+)\1", ('font', 'content')),
    # rawtext = ()  # default inline
)


def _get_depth(attr, type):
    """
    children을 가지는 block의 depth를 출력: 0: depth 없음, root / 1: 1차 하위 depth
    """
    if '_leading' not in attr:
        return 0
    elif type == 'quote':
        return attr['_leading'].count('>') - 1  # depth = 0 부터 시작
    elif type == 'bulleted_listitem':
        return 1  # TODO: attr['_leading'] 앞에 있는 공백 문자 개수?
    elif type == 'todo_listitem':
        return 1  # TODO: attr['_leading'] 앞에 있는 공백 문자 개수?
    elif type == 'numbered_listitem':
        return 1  # TODO: attr['_leading'] 의 구조에 따라? [1., 1), 1-1)], ...


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
    if depth == 0:
        if PATH_SEP not in line[0] and type in line[0]:
            return True
    elif type != line[0].rsplit(PATH_SEP, 1)[-1].rsplit(COUNT_SEP, 1)[0]:  # NOTE: type이 다른 경우, TODO: 확인 필요
        return False
    elif depth == line[0].count(PATH_SEP):  # depth 0부터
        return True
    else:
        return False


def _previous_sibling_path(type, depth, buff_lines):
    """형제 path
    """
    # lines.reverse()
    # _buff_lines = copy.deepcopy(buff_lines)
    for line in reversed(buff_lines):
        if _is_sibling(type, depth, line):
            return line[0]
        # # print(f"_previous_sibling_path line[0]: {line[0]}")
        # if depth == 0:
        #     # print(f"_previous_sibling_path line: {line}")
        #     if PATH_SEP not in line[0] and type in line[0]:
        #         return line[0]
        # elif type != line[0].rsplit(PATH_SEP, 1)[-1].rsplit(COUNT_SEP, 1)[0]:  # NOTE: type이 다른 경우, TODO: 확인 필요
        #     return None
        # elif depth == line[0].count(PATH_SEP):  # depth 0부터
        #     return line[0]

    return None


def _get_type_count_depth(path):
    """path -> type, count
    """
    depth = path.count(PATH_SEP)
    last = path.rsplit(PATH_SEP, 1)[-1]
    (type, count) = last.rsplit(COUNT_SEP, 1)  # NOTE: (type, count)
    return (type, count, depth)


def _set_path(type, depth, buff_lines):
    """path 설정
    """
    for line in reversed(buff_lines):
        if _is_sibling(type, depth, line):
            (_path, sn) = line[0].rsplit(COUNT_SEP, 1)  # NOTE: linebreak
            return f"{_path}{COUNT_SEP}{int(sn)+1}"
        elif depth > 0 and _is_sibling(type, depth-1, line):
            return f"{line[0]}{PATH_SEP}{type}{COUNT_SEP}0"
        # parent_path = _parent_path(type, depth, buff_lines)

    return f"{type}{COUNT_SEP}0"
    # # print(f"type: {type}, depth: {depth}, sibling: {sibling}", "%"*20)
    # if not sibling:
    #     parent_path = _parent_path(type, depth, buff_lines)
    #     # print("_set_path NOT sibling", f"{parent_path}{PATH_SEP}{type}{COUNT_SEP}0" if parent_path else f"{type}{COUNT_SEP}0")
    #     return f"{parent_path}{PATH_SEP}{type}{COUNT_SEP}0" if parent_path else f"{type}{COUNT_SEP}0"
    # else:
    #     (_path, sn) = (type, -1) if not sibling else sibling.rsplit(COUNT_SEP, 1)  # NOTE: linebreak
    #     print("_set_path WITH sibling", f"{_path}{COUNT_SEP}{int(sn)+1}")
    #     return f"{_path}{COUNT_SEP}{int(sn)+1}"


def _parent_path(type, depth, buff_lines):  # TODO(X): depth를 path에 표시  quote/1-1:quote/2-1: 
    """부모 path
    """
    return _previous_sibling_path(type, depth-1, buff_lines)


# def _find_parent(type, depth, lines):  # TODO(X): depth를 path에 표시  quote/1-1:quote/2-1: 
#     """부모 path
#     """
#     depth = depth-1
#     lines.reverse()
#     for line in lines:
#         if line[0] == path:
#             return line


def _append_children(path, type, depth, buff_lines):
    """path를 parent의 children에 추가
    """
    parent_path = path.rsplit(PATH_SEP, 1)[0]
    # parent_path = _parent_path(type, depth, buff_lines)
    buff_lines.reverse()
    for line in buff_lines:
        if line[0] == parent_path:
            line[2].append(path)
    buff_lines.reverse()  # linse 리스트 재역순
    return buff_lines


def _set_attr(attr):
    """attr에서 key가 '_'로 시작하는 값 제거 ex) _leading, _level 등
    """
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
            return (type, {attr: match.group(i+1) for i, attr in enumerate(attrs)})

    return ('paragraph', {'content': line})  # NOTE: type이 없다면 'paragraph'로 설정


def _document_to_lines(document, repls={}):
    """document -> lines
    TODO: 전처리: rstrip(), \n{3,} -> \n\n
    """
    return document.splitlines()


def _convert_block(type, attr):
    """type에 맞는 block template(dict)에 attr 값을 삽입
    """
    _dict = block_objects[type] if type in block_objects else block_objects['_default']
    s = str(_dict)
    s = s.replace("{type}", type)
    for k, v in attr.items():
        s = s.replace(f"{{{k}}}", v.replace("\n", "\\n"))  ## NOTE: 개행문자로 인한 오류 방지
    s = re.sub(r"': '\{.+\}'", "': None", s)  ## NOTE: TODO: content를 변경해버릴 가능성은? code block?
    return eval(s)


def parse_block(lines):
    # lines = document.splitlines()
    # buff_lines = [("linebreak-0", {'content': ''}, [])]  ## (path, value, children)
    buff_lines = [{"linebreak-0": {'content': '', 'children': []}}]  ## (path, value, children)

    for line in lines:
        (path, attr, children) = buff_lines[-1]  ## NOTE: 이전 라인 path, attr, children
        # (path, attr, children) = buff_lines[-1]  ## NOTE: 이전 라인 path, attr, children
        last = path.rsplit(PATH_SEP, 1)[-1]
        (type, count) = last.rsplit(COUNT_SEP, 1)
        (parse_text, multi_line, join_line, has_children, breakers) = block_settings[type]
        # print(f"has_children: {has_children}", "-"*80)

        ## path 변경(new, child) / value JOIN
        if line.strip() in breakers:  ## 현재 라인이 linebreaker에 해당하면, 블럭 초기화, TODO: 연속으로 null 블럭("linebreak", {'content': ''}, [])이 나오는 것은 없앨 것
            print("현재 라인이 linebreaker", "-"*80)
            if type != 'linebreak':
                buff_lines.append((_set_path('linebreak', 0, buff_lines), {'content': ''}, []))
            continue
        else:
            (_type, _attr) = _line_type_attr(line)  # 현재 라인 type, attr
            _depth = _get_depth(_attr, _type)
            if type != 'linebreak' and not parse_text:
                attr['content'] = attr.get('content', '')
                attr['content'] += '\n' + _attr['content']
            elif (type == 'linebreak') or (not multi_line) or (type != _type):  ## 새로운 블럭(루트)인 경우(현재 라인이 linebreak / 이전 라인이 multi_line이 안되는 경우 / 현재 라인과 이전 라인의 type이 다른 경우)
                # print("새로운 블럭(루트)인 경우", "-"*80)
                buff_lines.append((_set_path(_type, 0, buff_lines), _set_attr(_attr), []))  # root block(line) 추가
            elif not has_children:  ## 이전 라인이 자식을 갖지 않을 경우 -> 이전 라인의 부모가 있는지 확인
                if join_line:  # content만 추가
                    attr['content'] += '\n' + _attr['content']
                else:  # 형제 line 생성
                    buff_lines.append((_set_path(_type, _depth, buff_lines), _set_attr(_attr), []))
            elif has_children:  ## TODO: else로 전환?
                # _depth = _get_depth(_attr, _type)
                if _depth == 0: ## TODO: 확인 필요, depth가 없거나, root 블럭(depth=1)인 경우
                    print(f"root DEPTH: _depth: {_depth} path: {path} _attr['_leading']: {_attr['_leading']}", "*"*80)
                    # _attr['depth'] = _depth
                    buff_lines.append((_set_path(_type, _depth, buff_lines),  _set_attr(_attr), []))
                # elif _get_depth(_attr, _type) > _get_depth(attr, type): ## 이전 라인의 자식 블럭인 경우(depth)
                else:
                    if not join_line or _depth != path.count(PATH_SEP):
                        _path = _set_path(_type, _depth, buff_lines)
                        # print(f"Append Children: {_path}")
                        _append_children(_path, _type, _depth, buff_lines)  # TODO: 제대로 작동하지는 확인 필요!!!
                        # _attr['depth'] = _depth
                        buff_lines.append((_path,  _set_attr(_attr), []))
                    else:  # NOTE: line join
                        attr['content'] += '\n' + _attr['content']

    return buff_lines


def parse_line(line):  # inline / block(single_line) heading, paragraph(1 line)
    return line


# def _find_parsed_line(path):
#     pass


# def _append_child_dict(_dict, child_dict, parsed_lines):
#     if not child_dict['children']:
#         _dict.append(child_dict)
#     else:
#         _grandson_dict
#         _append_child_dict(child_dict, _grandson_dict, parsed_lines)


def convert_document(parsed_lines):
    """parsed_lines -> object(dict) list
    """
    parsed_document = []
    for (path, attr, children) in parsed_lines:
        (type, count, depth) = _get_type_count_depth(path)
        _dict = _convert_block(type, attr)
        if not children:
            parsed_document.append(_dict)
        else:  # NOTE: 자식 라인이 있는 경우
            for child in children:
                pass
                # 1. 자식 노드가 자식을 가지고 있는가?
                # 2. 가지고 있지 않다면 append_children
                # 3. 가지고 있다면 append_children 재귀 호출
    return parsed_document


## NOTE: TEST

lines = [
    "# heading_1-0 *italic* **bold** test",
    # "```python",
    # "    def fun(a):",
    # "         return a^2",
    # "```",
    # "paragraph-0  *italic* **bold** test",
    # "paragraph-1  *italic* **bold** test",
    "## heading_2-0 *italic* **bold** test",
    "> quote0  *italic* **bold** test",
    "> > quote0-0  *italic* **bold** test",
    "> > quote0-1  *italic* **bold** test",
    "> quote1  *italic* **bold** test",
    "> > quote1-0  *italic* **bold** test",
    "> > > quote1-0-1  *italic* **bold** test",
    "> > > quote1-0-2  *italic* **bold** test",
    "> > quote1-1  *italic* **bold** test",

    # "# heading_1-1 *italic* **bold** test",
]

buff_lines = parse_block(lines)
# print(buff_lines)


r = convert_document(buff_lines)
print(r)

# type = "quote"
# attr = dict(content="test quote")
# r = _convert_block(type, attr)
# print(r)
# lines = parse_block(document)

# parsed_document = []

# for line in lines:
#     parsed_document.append(parse_line(line))

# convert_document(parsed_document)
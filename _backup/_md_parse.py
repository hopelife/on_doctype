# -*- coding: utf-8 -*-

# https://gist.github.com/felko/1c06929ef9a395dfde7e
import re
from collections import OrderedDict
from string import Template

BASE_HTML = Template("""<!DOCTYPE html><!-- $TITLE, $TYPE written by $AUTHOR --><head><title>$TITLE</title><meta charset="$ENCODE"/><style>body{font-family:$FONT;}.underlined{text-decoration: underline;}.obfuscated{text-decoration:line-through;}.centered{text-align:center;}table{border-collapse:collapse;}th{border:1px solid black;padding:5px;background-color:#DDDDDD;}td{border:1px solid black;padding:5px;}</style></head><body>$html</body>""")

class Token:
    def __init__(self, regex):
        self.regex = regex

tokens = OrderedDict()

class token:
    def __init__(self, regex, subparse=True):
        self.regex = regex
        self.subparse = subparse

    def __call__(self, fn):
        from functools import wraps

        new_token = Token(self.regex)
        new_token.parse = fn
        tokens[fn.__name__] = new_token

        @wraps(fn)
        def wrapper(match):
            if self.subparse:
                return subparse(fn(match))
            else:
                return fn(match)
        return wrapper

@token(r"""(?P<spec>\$_(?P<name>.+)\((?P<value>.*)\))\n""", subparse=False)
def spec(match): return ''

@token(r"""(?<!\*)\*(?!\*)(?P<em>[^\s].+?[^\s])(?<!\*)\*(?!\*)""")
def em(match):
    return '<em>{em}</em>'.format(**match)

@token(r"""\*\*(?P<strong>[^\s].+?[^\s])\*\*""")
def strong(match):
    return '<strong>{strong}</strong>'.format(**match)

@token(r"""_(?P<underlined>[^\s].+?[^\s])_""")
def underlined(match):
    return '<span class="underlined">{underlined}</span>'.format(**match)

@token(r"""-(?P<obfuscated>[^\s].+?[^\s])-""")
def obfuscated(match):
    return '<span class="obfuscated">{obfuscated}</span>'.format(**match)

@token(r"""(?<!`)`(?!`)(?P<code>[^\s].+?[^\s])(?<!`)`(?!`)""")
def code(match):
    return '<code>{code}</code>'.format(**match)

@token(r"""#(?P<h1>.+)\n""")
def h1(match):
    return '<h1>{h1}</h1>'.format(**match)

@token(r"""##(?P<h2>.+)\n""")
def h2(match):
    return '<h2>{h2}</h2>'.format(**match)

@token(r"""###(?P<h3>.+)\n""")
def h3(match):
    return '<h3>{h3}</h3>'.format(**match)

@token(r"""####(?P<h4>.+)\n""")
def h4(match):
    return '<h4>{h4}</h4>'.format(**match)

@token(r"""#####(?P<h5>.+)\n""")
def h5(match):
    return '<h5>{h5}</h5>'.format(**match)

@token(r"""(?P<a>\[(?P<disp>.+)\] *\((?P<href>[^ \n]+)\))""")
def a(match):
    return '<a href="{href}">{disp}</a>'.format(**match)

@token(r"""\n%(?P<anchor>\w+)%""")
def anchor(match):
    return '<div id="{anchor}"></>'.format(**match)

@token(r"""\^(?P<centered>[^\s].*?[^\s])\^""")
def centered(match):
    return '<div class="centered">{centered}</div>'.format(**match)

@token(r"""_\((?P<sub>.+?)\)""")
def sub(match):
    return '<sub>{sub}</sub>'.format(**match)

@token(r"""\^\((?P<sup>.+?)\)""")
def sup(match):
    return '<sup>{sup}</sup>'.format(**match)

@token(r"""(?:```(?P<class>.*)(?P<pre>(?:.|\n)+?)```)""")
def pre(match):
    return '<pre' +\
           ' class="{class}"' * bool(len(match['class'])) +\
           '>{pre}</pre>'.format(**match)

@token(r"""{table:\n*(?P<table>(?:.|\n)*?)}""")
def table(match):
    return '<table>{table}</table>'.format(table=parse_table(match['table']))

@token(r"""(?P<br>\n)""")
def br(match):
    return '<br/>'

@token(r"""(?P<mismatch>.|\n)""")
def mismatch(match):
    return '{mismatch}'.format(**match)

#--------- Parsing ----------

reg_list = [tok.regex for tok in tokens.values()]
markup_regex = re.compile('|'.join(reg_list))


def translate(raw_md, base=BASE_HTML, **default):
    default['html'] = ''
    matches = re.finditer(markup_regex, raw_md)
    for token in matches:
        kind = token.lastgroup
        if kind == 'spec':
            name, value = token.group('name'), token.group('value')
            default[name] = value
        value = token.groupdict()
        default['html'] += tokens[kind].parse(value)
    if isinstance(base, Template):
        return base.substitute(**default)
    else:
        return base.format(**default)


def subparse(match):
    subhtml, all_mismatch = '', True
    matches = re.finditer(markup_regex, raw_md)
    for token in matches:
        kind = token.lastgroup
        if kind is 'mismatch':
            all_mismatch = False
        value = token.groupdict()
        subhtml += tokens[kind].parse(value)
    if all_mismatch:
        return subhtml
    else:
        return subparse(subhtml)


def parse_table(table):
    def tr_parse(tr):
        tr_html = ''
        table_regexes = OrderedDict([
            ('td', r"""(?P<td>(?<=\|)(?!:).*?(?<!:)(?=\|))"""),
            ('th', r"""(?P<th>(?<=\|:).*?(?=:\|))""")
        ])
        markup_format = {
            'td': lambda **kwds: '<td>{td}</td>'.format(**kwds),
            'th': lambda **kwds: '<th>{th}</th>'.format(**kwds),
        }

        tr_sub = re.compile('|'.join(
            ['(?:{})'.format(reg) for reg in table_regexes.values()]))
        for elt in re.finditer(tr_sub, tr):
            kind = elt.lastgroup
            value = elt.groupdict()
            tr_html += markup_format[kind](**value)
        return tr_html

    rows = ''
    tr_re = re.compile(r"""(?P<tr>.+(?=\n[+-]+))""")
    for tr in tr_re.findall(table):
        rows += '<tr>{}</tr>'.format(tr_parse(tr))
    return rows


if __name__ == '__main__':
    import sys
    file_path, dest_path = sys.argv[1:]
    with open(file_path) as file:
        raw_md = file.read()
    with open(dest_path, 'w') as dest:
        html = translate(raw_md)
        dest.write(html)
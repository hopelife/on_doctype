# https://github.com/OpenBapul/hml-equation-parser
# https://meetup.toast.com/posts/311
# http://www.malinc.se/math/latex/basiccodeen.php

## notion
# [14. 수식을 씁시다!](https://www.notion.so/14-1f5fa00916414a43b4c7d77ee7dcf9ed)
# https://www.notion.so/a5e4fb79dd7646c78072a1d214cd0038#617817f69bb2472ba125a5332d13d072
# https://www.math.brown.edu/johsilve/ReferenceCards/TeXRefCard.v1.5.pdf

## TEX
# [Comprehensive TEX Archive Network](https://ctan.org/)
# [한국 TEX 사용자 그룹](http://www.ktug.org/xe/)
# https://katex.org/docs/supported.html
# [Visual Studio Code 활용한 LATEX 사용기 - 1장 설치](https://success-now.tistory.com/17)
# [LATEX in VS Code](https://jangsookim.github.io/lectures/vscode/vscode_lecture0.html)
# https://jangsookim.github.io/lectures/vscode/vscode_lecture1.html

# 환경 설정 path: C:\texlive\2022\bin\win32

# https://www.overleaf.com/latex/examples/tikz-airplane-picture/vjpvcmtnqcnx

# https://texample.net/tikz/examples/area/mathematics/

# [Visual Studio Code를 사용하여 편리한 LaTeX 환경 구축하기 - Lecture 1](https://www.youtube.com/watch?v=aSdGb47jJtc)

# [LaTeX 특강: TikZ](https://www.youtube.com/watch?v=UwrTjXxWD14)
# [tikz online](https://tikzcd.yichuanshen.de/)
# [TikZ와 수학](http://wiki.ktug.org/wiki/wiki.php/LaTexWorkshop/2017)



# https://martinii.fun/220

## TikZ
# https://ko.overleaf.com/learn/latex/TikZ_package
# https://texample.net/tikz/examples/area/mathematics/
# https://texample.net/tikz/resources/
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=wool613&logNo=221511340406

## mathML
# https://ko.overleaf.com/latex/examples/figures-tikz-du-cours-notions-de-probabilite/qmbtssgknzjk
# https://femto-physique.fr/physique_statistique/phystat_complement1.php


import os
import shutil
# import xml.etree.ElementTree as ET
import lxml.etree as et
import re

EQ_MAP = {
  "convertMap": {
    # <A> over <B> -> \\frac{A}{B}
    # barBD, bar BD, bar {BD}  -> \\overline{BD}

    "TIMES": "\\times",
    "times": "\\times",
    "LEFT": "\\left",
    "RIGHT": "\\right",
    "under": "\\underline",
    "SMALLSUM": "\\sum",
    "sum": "\\sum",
    "SMALLPROD": "\\prod",
    "prod": "\\prod",
    "SMALLINTER": "\\cap",
    "CUP": "\\cup",
    "OPLUS": "\\oplus",
    "OMINUS": "\\ominus",
    "OTIMES": "\\otimes",
    "ODIV": "\\oslash",
    "ODOT": "\\odot",
    "LOR": "\\lor",
    "LAND": "\\land",
    "SUBSET": "\\subset",
    "SUPERSET": "\\supset",
    "SUBSETEQ": "\\subseteq",
    "SUPSETEQ": "\\supseteq",
    "IN": "\\in",
    "OWNS": "\\owns",
    "NOTIN": "\\notin",
    "LEQ": "\\leq",
    "GEQ": "\\geq",
    "<<": "\\ll",
    ">>": "\\gg",
    "<<<": "\\lll",
    ">>>": "\\ggg",
    "PREC": "\\prec",
    "SUCC": "\\succ",
    "UPLUS": "\\uplus",
    "±": "\\pm",
    "-+": "\\mp",
    "÷": "\\div",
    "CIRC": "\\circ",
    "BULLET": "\\bullet",
    "DEG": " ^\\circ",
    "AST": "\\ast",
    "STAR": "\\bigstar",
    "BIGCIRC": "\\bigcirc",
    "EMPTYSET": "\\emptyset",
    "THEREFORE": "\\therefore",
    "BECAUSE": "\\because",
    "EXIST": "\\exists",
    "!=": "\\neq",
    "SMCOPROD": "\\coprod",
    "coprod": "\\coprod",
    "SQCAP": "\\sqcap",
    "SQCUP": "\\sqcup",
    "SQSUBSET": "\\sqsubset",
    "SQSUBSETEQ": "\\sqsubseteq",

    "BIGSQCUP": "\\bigsqcup",
    "BIGOPLUS": "\\bigoplus",
    "BIGOTIMES": "\\bigotimes",
    "BIGODOT": "\\bigodot",
    "BIGUPLUS": "\\biguplus",

    "inter": "\\bigcap",
    "union": "\\bigcup",
    "BIGOMINUS": "{\\Large\\ominus}",
    "BIGODIV": "{\\Large\\oslash}",
    "UNDEROVER": "",

    "SIM": "\\sim",
    "APPROX": "\\approx",
    "SIMEQ": "\\simeq",
    "CONG": "\\cong",
    "==": "\\equiv",
    "DIAMOND": "\\diamond",
    "FORALL": "\\forall",
    "prime": "'",
    "Partial": "\\partial",
    "INF": "\\infty",
    "PROPTO": "\\propto",
    "lim": "\\lim",
    "Lim": "\\lim",
    "larrow": "\\leftarrow",
    "->": "\\rightarrow",
    "uparrow": "\\uparrow",
    "downarrow": "\\downarrow",
    "LARROW": "\\Leftarrow",
    "RARROW": "\\Rightarrow",
    "UPARROW": "\\Uparrow",
    "DOWNARROW": "\\Downarrow",
    "udarrow": "\\updownarrow",
    "<->": "\\leftrightarrow",
    "UDARROW": "\\Updownarrow",
    "LRARROW": "\\Leftrightarrow",
    "NWARROW": "\\nwarrow",
    "SEARROW": "\\searrow",
    "NEARROW": "\\nearrow",
    "SWARROW": "\\swarrow",
    "HOOKLEFT": "\\hookleftarrow",
    "HOOKRIGHT": "\\hookrightarrow",
    "PVER": "\\|",
    "MAPSTO": "\\mapsto",
    "CDOTS": "\\cdots",
    "LDOTS": "\\ldots",
    "VDOTS": "\\vdots",
    "DDOTS": "\\ddots",
    "DAGGER": "\\dagger",
    "DDAGGER": "\\ddagger",
    "DOTEQ": "\\doteq",

    "image": "\\fallingdotseq",
    "REIMAGE": "\\risingdotseq",
    "ASYMP": "\\asymp",
    "ISO": "\\Bumpeq",
    "DSUM": "\\dotplus",
    "XOR": "\\veebar",
    "TRIANGLE": "\\triangle",
    "NABLA": "\\nabla",
    "ANGLE": "\\angle",
    "MSANGLE": "\\measuredangle",
    "SANGLE": "\\sphericalangle",
    
    "VDASH": "\\vdash",
    "DASHV": "\\dashv",
    "BOT": "\\bot",
    "TOP": "\\top",
    "MODELS": "\\models",
    "LAPLACE": "\\mathcal{L}",
    "CENTIGRADE": "^{\\circ}C",
    "FAHRENHEIT": "^{\\circ}F",
    "LSLANT": "\\diagup",
    "RSLANT": "\\diagdown",

    "sqrt": "\\sqrt",
    "int": "\\int",
    "dint": "\\iint",
    "tint": "\\iiint",
    "oint": "\\oint",
    "alpha": "\\alpha",
    "beta": "\\beta",
    "gamma": "\\gamma",
    "delta": "\\delta",
    "epsilon": "\\epsilon",
    "zeta": "\\zeta",
    "eta": "\\eta",
    "theta": "\\theta",
    "iota": "\\iota",
    "kappa": "\\kappa",
    "lambda": "\\lambda",
    "mu": "\\mu",
    "nu": "\\nu",
    "xi": "\\xi",
    "omicron": "\\omicron",
    "pi": "\\pi",
    "rho": "\\rho",
    "sigma": "\\sigma",
    "tau": "\\tau",
    "upsilon": "\\upsilon",
    "phi": "\\phi",
    "chi": "\\chi",
    "psi": "\\psi",
    "omega": "\\omega",
    "ALPHA": "A",
    "BETA": "B",
    "GAMMA": "\\Gamma",
    "DELTA": "\\Delta",
    "EPSILON": "E",
    "ZETA": "Z",
    "ETA": "H",
    "THETA": "\\Theta",
    "IOTA": "I",
    "KAPPA": "K",
    "LAMBDA": "\\Lambda",
    "MU": "M",
    "NU": "N",
    "XI": "\\Xi",
    "OMICRON": "O",
    "PI": "\\Pi",
    "RHO": "P",
    "SIGMA": "\\Sigma",
    "TAU": "T",
    "UPSILON": "\\Upsilon",
    "PHI": "\\Phi",
    "CHI": "X",
    "PSI": "\\Psi",
    "OMEGA": "\\Omega",

    "⌈": "\\lceil",
    "⌉": "\\rceil",
    "⌊": "\\lfloor",
    "⌋": "\\rfloor",
    "∥": "\\|",
    "⊐": "\\sqsupset",
    "⊒": "\\sqsupseteq",

    "odint": "\\mathop ∯",
    "otint": "\\mathop ∰",
    "BIGSQCAP": "\\mathop ⨅",
    "ATT": "\\mathop ※",
    "HUND": "\\mathop ‰",
    "THOU": "\\mathop ‱",
    "IDENTICAL": "\\mathop ∷",
    "RTANGLE": "\\mathop ⊾",
    "BASE": "\\mathop ⌂",
    "BENZENE": "\\mathop ⌬"
  },

  "middleConvertMap": {
    "matrix": "HULKMATRIX",
    "pmatrix": "HULKPMATRIX",
    "bmatrix": "HULKBMATRIX",
    "dmatrix": "HULKDMATRIX",
    "eqalign": "HULKEQALIGN",
    "cases": "HULKCASE",
    "vec": "HULKVEC",
    "dyad": "HULKDYAD",
    "acute": "HULKACUTE",
    "grave": "HULKGRAVE",
    "dot": "HULKDOT",
    "ddot": "HULKDDOT",
    "bar": "HULKBAR",
    "hat": "HULKHAT",
    "check": "HULKCHECK",
    "arch": "HULKARCH",
    "tilde": "HULKTILDE",
    "BOX": "HULKBOX",
    "OVERBRACE": "HULKOVERBRACE",
    "UNDERBRACE": "HULKUNDERBRACE"
  },

  "BarConvertMap": {
    "HULKVEC": "\\overrightarrow",
    "HULKDYAD": "\\overleftrightarrow",
    "HULKACUTE": "\\acute",
    "HULKGRAVE": "\\grave",
    "HULKDOT": "\\dot",
    "HULKDDOT": "\\ddot",
    "HULKBAR": "\\overline",
    "HULKHAT": "\\widehat",
    "HULKCHECK": "\\check",
    "HULKARCH": "\\overset{\\frown}",
    "HULKTILDE": "\\widetilde",
    "HULKBOX": "\\boxed"
  },

  "MatrixConvertMap": {
    "HULKMATRIX": {
      "begin": "\\begin{matrix}",
      "end": "\\end{matrix}",
      "removeOutterBrackets": True
    },

    "HULKPMATRIX": {
      "begin": "\\begin{pmatrix}",
      "end": "\\end{pmatrix}",
      "removeOutterBrackets": True
    },

    "HULKBMATRIX": {
      "begin": "\\begin{bmatrix}",
      "end": "\\end{bmatrix}",
      "removeOutterBrackets": True
    },

    "HULKDMATRIX": {
      "begin": "\\begin{vmatrix}",
      "end": "\\end{vmatrix}",
      "removeOutterBrackets": True
    },

    "HULKCASE": {
      "begin": "\\begin{cases}",
      "end": "\\end{cases}",
      "removeOutterBrackets": True
    },

    "HULKEQALIGN": {
      "begin": "\\eqalign{",
      "end": "}",
      "removeOutterBrackets": False
    }
  },

  "BraceConvertMap": {
    "HULKOVERBRACE": "\\overbrace",
    "HULKUNDERBRACE": "\\underbrace"
  }
}


# with open(r"C:\Dev\__pyon\on_doctype\_data\hwp\핵심정리 (수10)_문정삼\Contents\section0.xml", "r", encoding="utf-8") as f:
#     xml = re.sub(r"<\?[^>?]+\?>", "", f.read())  # NOTE: 선언 부분 제외
# # root = etree.XML("<root>data</root>")
# root = etree.XML(xml)

root = et.parse(r"C:\Dev\__pyon\on_doctype\_data\hwp\핵심정리 (수10)_문정삼\Contents\section0.xml")

# print(root.tag)
# print(root.tostring())
# print(et.tostring(root, pretty_print=True))

# 텍스트: hp:p/hp:run/hp:t
# 수식: hp:p/hp:run/hp:equation/hp:script

ps = root.xpath("//hp:p/hp:run", namespaces={'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph'})

# print(f"{ps=}")

# 텍스트: hp:p/hp:run/hp:t
# 수식: hp:p/hp:run/hp:equation/hp:script
# 컨테이너: hp:p/hp:run/hp:container
# 테이블?: hp:p/hp:run/hp:tbl
# hp:drawText
# hp:rect


for p in ps:
    for child in p:
        # if child.tag.rsplit("}", 1)[1] == 'equation':
        if child.tag.endswith('}equation'):
            equation = child.xpath(".//text()")
            # print("-"*60)
            if equation:
                equation = " ".join(equation)
                # print(f"{equation=}")
                for k, v in EQ_MAP['convertMap'].items():
                    # print(f"{k=} {v=}")
                    equation = re.sub(rf"\b{k}\b", v.replace("\\", "\\\\"), equation, flags=re.IGNORECASE)
            print(f'수식: ${equation.strip()}$')
            # print(f'수식: {child.xpath(".//text()")=}')
        else:
            pass
            # print(f'수식외: {child.xpath(".//text()")=}')
            ## TODO: grandson equation
            # if child.text:
            #     print(f"수식외: {child.text=}")
    # 수식  hp:equation
    # hp:container

    # 수식 이외
    # print(f'{p.xpath(".//text()")=}')

# for el in root.xpath("//hp:p"):
#     print(f"{el.text=}")
# #4
# tree = ET.parse(r"C:\Dev\__pyon\on_doctype\_data\hwp\핵심정리 (수10)_문정삼\Contents\section0.xml")
# root = tree.getroot()

# print(root)
# for child in root.iter():
#     print(f"{child.tag=}")
#     if child.tag == "hp:p":
#     # if child.tag == "hp:p":
#     #     print("paragraph")
# # #5
# # tbl_list = []
# # for child in root.iter():
# #     if child.tag.endswith("}tbl"):
# #         tbl_list.append(child)

# # #6
# # tbl = tbl_list[0]
# # tbl_cols = int(tbl.attrib["colCnt"])
# # tbl_rows = int(tbl.attrib["rowCnt"])


# # #7
# # data = []
# # for i in tbl.iter():
# #     if i.tag.endswith("}t"):
# #         data.append(i.text)

# # print(data)
# # #8
# # df = pd.DataFrame(data)
# # df = pd.DataFrame(data=df.iloc[tbl_cols:, :].values.reshape(-1, tbl_cols), columns=df.iloc[:tbl_cols, 0].values)
# # df = df.astype({"total_bill": "float", "tip": "float", "size": "int"})


# #9
# # shutil.rmtree(path)

# # 끝.



# # ### 플로팅
# # df.describe()

# # import seaborn as sns
# # import matplotlib.pyplot as plt

# # plt.style.use('ggplot')
# # sns.catplot(x="day", y="total_bill", hue="sex", kind="violin", data=df)
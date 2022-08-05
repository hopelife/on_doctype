# https://martinii.fun/220
# https://github.com/OpenBapul/hml-equation-parser

import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

# import pandas as pd


#2
hwpx_file = r"C:\Users\user\Downloads\한글컨트롤 프로그래밍 이해와 활용.hwpx"
os.chdir(os.path.dirname(hwpx_file))
path = os.path.join(os.getcwd(), "hwpx")

#3
with zipfile.ZipFile(hwpx_file, 'r') as zf:
    zf.extractall(path=path)

#4
tree = ET.parse(os.path.join(os.getcwd(), "hwpx", "Contents", "section0.xml"))
root = tree.getroot()

print(root)
# #5
# tbl_list = []
# for child in root.iter():
#     if child.tag.endswith("}tbl"):
#         tbl_list.append(child)

# #6
# tbl = tbl_list[0]
# tbl_cols = int(tbl.attrib["colCnt"])
# tbl_rows = int(tbl.attrib["rowCnt"])


# #7
# data = []
# for i in tbl.iter():
#     if i.tag.endswith("}t"):
#         data.append(i.text)

# print(data)
# #8
# df = pd.DataFrame(data)
# df = pd.DataFrame(data=df.iloc[tbl_cols:, :].values.reshape(-1, tbl_cols), columns=df.iloc[:tbl_cols, 0].values)
# df = df.astype({"total_bill": "float", "tip": "float", "size": "int"})


#9
shutil.rmtree(path)

# 끝.



# ### 플로팅
# df.describe()

# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.style.use('ggplot')
# sns.catplot(x="day", y="total_bill", hue="sex", kind="violin", data=df)
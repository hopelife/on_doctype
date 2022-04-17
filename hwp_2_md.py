# C:\Dev\on_document\_reference\hwp\한글문서파일형식_5.0_revision1.3.hwp

import os
import win32com.client as win32

path = r"C:\Dev\on_document\_reference\hwp\한글컨트롤 사용법\한글컨트롤 프로그래밍 이해와 활용.hwp"

# 한/글 개체 생성
hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")

hwp.Open(path, "HWP", "forceopen:true")

# 원하는 작업을 수행합니다. 

hwp.Run("SelectAll") # 전체 선택
hwp.Run("Copy") # 복사
# hwp.MovePos(3) 맨 뒤로 이동
# hwp.Run("Erase") # 지우기
# hwp.Run("PasteSpecial") # 골라 붙이기
# hwp.Run("Cancel") # esc

# # 수정된 파일을 저장하고 나갑니다. 

# hwp.Save()
# hwp.Quit()


# import win32com.client as win32
# import win32gui

# hwp = win32.Dispatch('HWPFrame.HwpObject')
# hwnd = win32gui.FindWindow(None, "빈 문서 1 - 한글")

# hwp.XHwpWindows.Item(0).Visible = True

# print(hwnd)

# def write(s):
#     act=hwp.CreateAction("InsertText")
#     set=act.CreateSet()
#     act.GetDefault(set)
#     set.SetItem("Text",s)
#     ret=act.Execute(set)

# write("성공")

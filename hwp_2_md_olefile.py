# C:\Dev\on_document\_reference\hwp\한글문서파일형식_5.0_revision1.3.hwp

import olefile
# import pandas as pd

f = olefile.OleFileIO(r"C:\Dev\on_document\_reference\hwp\한글컨트롤 사용법\한글컨트롤 프로그래밍 이해와 활용.hwp")
#PrvText 스트림 내의 내용을 읽기
encoded_text = f.openstream('PrvText').read() 
#인코딩된 텍스트를 UTF-16으로 디코딩
decoded_text = encoded_text.decode('UTF-16') 

print(decoded_text)

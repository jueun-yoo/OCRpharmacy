import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 로드
image_path = "3.jpg" #이미지 경로임 추후 수정 필요!!
img = cv2.imread(image_path)

# 그레이 스케일 변환
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 빛 반사-CLAHE 객체 생성
clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(4,4))

# 빛 반사-CLAHE 적용
img_clahe = clahe.apply(img_gray)

# 가우시안 블러 적용 
img_blur = cv2.GaussianBlur(img_clahe, (3, 3), 0)

# Adaptive 이진화 적용
img_adaptive = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=3, C=3)

# 노이즈 제거
img_denoise = cv2.fastNlMeansDenoising(img_adaptive)

# 색상 반전
img_inverted = cv2.bitwise_not(img_denoise)

# 결과 이미지 저장 및 출력
cv2.imwrite("result3.jpg", img_inverted) #결과 이미지 이름임 추후 수정 필요!!
cv2.imshow("Result", img_inverted)
cv2.waitKey(0)
cv2.destroyAllWindows()
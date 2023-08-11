from django.shortcuts import render, get_object_or_404, redirect
from .models import Nutrient, Supplement, RecommendedIntake, Synonym
from .forms import SupplementForm, ImageUploadForm, OCRResultEditForm
import cv2
import uuid
import json
import time
import requests
import sqlite3
from PIL import Image, ImageDraw
from io import BytesIO  # io 모듈에서 BytesIO를 import 합니다.

# Create your views here.
# 영양소 상세 보기
def nutrient_detail(request, nutrient_id):
    nutrient = get_object_or_404(Nutrient, pk=nutrient_id)
    return render(request, 'nutrient_detail.html', {'nutrient': nutrient})

# 영양소 상세 보기와 동의어 함께 보기
def nutrient_detail_with_synonyms(request, nutrient_id):
    nutrient = get_object_or_404(Nutrient, pk=nutrient_id)

    # OCR에서 가져온 영양소 표현 (예시로 "비타민B1"로 가정)
    ocr_expression = "비타민B1"

    # OCR로부터 가져온 표현이 "비타민B1"인 경우, "티아민"으로 변경
    if ocr_expression == "비타민B1":
        ocr_expression = "티아민"

    return render(request, 'nutrient_detail_with_synonyms.html', {'nutrient': nutrient, 'ocr_expression': ocr_expression})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .models import Supplement, Nutrient
from .models import Supplement, SupplementNutrient, RecommendedNutrient, Interaction

""" # Create your views here.
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
 """

def supplement_detail(request, supplement_id):
    supplement = get_object_or_404(Supplement, id=supplement_id)
    user = request.user

    supplement_nutrients = {sn.nutrient.name: sn.dosage for sn in SupplementNutrient.objects.filter(supplement=supplement)}
    recommended_nutrients = {rn.nutrient.name: rn.dosage for rn in RecommendedNutrient.objects.filter(recommended_intake=user.recommended)}


    nutrient_percentages = {}
    for nutrient, dosage in supplement_nutrients.items():
        recommended_dosage = recommended_nutrients.get(nutrient)
        if recommended_dosage:
            percentage = (dosage / recommended_dosage) * 100
            nutrient_percentages[nutrient] = percentage


    interactions = Interaction.objects.filter(nutrient1__in=supplement.nutrients.all(), nutrient2__in=supplement.nutrients.all())

    return render(request, 'supplements/supplement_detail.html', {
        'supplement': supplement,
        'nutrient_percentages': nutrient_percentages,
        'interactions': interactions
    })

def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        # 세션에 임시 이미지 URL 저장
        request.session['uploaded_file_url'] = uploaded_file_url

        return redirect('supplements:process_image')

###############정보추출함수 내놔..
def process_image(request):
    uploaded_file_url = request.session.get('uploaded_file_url')

    # 이미지에서 필요한 정보 추출 (정보추출 함수 필요)
    extracted_info = extract_info_from_image(uploaded_file_url)

    # 추출된 정보를 세션에 저장
    request.session['extracted_info'] = extracted_info

    return render(request, 'preview.html', {'info': extracted_info})

from django.shortcuts import render, redirect
from .models import Supplement, SupplementNutrient, Nutrient

def save_info(request):
    if request.method == 'POST':
        # 세션에서 추출된 정보를 가져옵니다.
        extracted_info = request.session.get('extracted_info')

        # Supplement 객체를 생성합니다.
        supplement = Supplement(name=extracted_info['name'], user=request.user)
        supplement.save()

        # 각 영양소 정보를 저장합니다.
        for nutrient_info in extracted_info['nutrients']:
            nutrient_name = nutrient_info['name']
            dosage = nutrient_info['dosage']
            unit = nutrient_info['unit']

            # 영양소를 찾거나 새로 생성합니다.
            nutrient, created = Nutrient.objects.get_or_create(name=nutrient_name)

            # SupplementNutrient 객체를 생성하고 연결합니다.
            supplement_nutrient = SupplementNutrient(nutrient=nutrient, supplement=supplement, dosage=dosage, unit=unit)
            supplement_nutrient.save()

        return redirect('success')

    return redirect('error')

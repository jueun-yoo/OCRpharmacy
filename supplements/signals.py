from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Supplement, SupplementNutrient, Nutrient
from user.models import UserTotalIntake

#영양제가 아니라, 영양소영양제 데이터가 추가될 때 마다 자동 갱신
@receiver(post_save, sender=SupplementNutrient)
def update_user_total_intake(sender, instance, **kwargs):
    nutrient = instance.nutrient
    dosage = instance.dosage
    user = instance.supplement.user

    # 사용자의 총 섭취량을 찾거나 새로 만듭니다.
    total_intake, created = UserTotalIntake.objects.get_or_create(
        user=user,
        nutrient=nutrient,
        defaults={'dosage': 0}
    )

    # 총 섭취량을 업데이트합니다.
    total_intake.dosage += dosage
    total_intake.save()

@receiver(post_save, sender=Supplement)
def create_supplement_nutrients(sender, instance, created, **kwargs):
    if created: # Supplement 객체가 처음 생성될 때만 실행
        for nutrient in Nutrient.objects.all():
            SupplementNutrient.objects.create(
                nutrient=nutrient,
                supplement=instance,
                dosage=0.0
            )
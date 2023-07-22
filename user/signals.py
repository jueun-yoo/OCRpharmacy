from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from supplements.models import RecommendedNutrient  # 적정영양소 모델 불러오기

@receiver(post_save, sender=User)
def assign_nutrition_pk(sender, instance=None, created=False, **kwargs):
    if created:
        recommended = RecommendedNutrient.objects.filter(
            age=instance.age, 
            gender=instance.gender,
            breastfeeding=instance.breastfeeding,
            pregnancy=instance.pregnancy
        ).first()

        if RecommendedNutrient:
            instance.recommended = RecommendedNutrient.pk
            instance.save()
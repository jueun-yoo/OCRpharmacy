from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from supplements.models import RecommendedIntake  # 적정영양소 모델 불러오기

User = get_user_model()

@receiver(post_save, sender=User)
def assign_recommended_intake(sender, instance=None, created=False, **kwargs):
    if created:
        recommended = RecommendedIntake.objects.filter(
            age_start__gte=instance.age,
            age_end__lte=instance.age,
            gender=instance.gender,
            breastfeeding=instance.breastfeeding,
            pregnancy=instance.pregnancy
        ).first()

        if RecommendedIntake:
            instance.recommended = recommended
            instance.save()
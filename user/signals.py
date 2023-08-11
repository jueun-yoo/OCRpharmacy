from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from supplements.models import Nutrient, UserTotalIntake, RecommendedIntake

User = get_user_model()

@receiver(post_save, sender=User)
def assign_recommended_intake(sender, instance=None, created=False, **kwargs):
    if created:
        recommended = RecommendedIntake.objects.filter(
            age_start__lte=instance.age,
            age_end__gte=instance.age,
            gender=instance.gender,
            breastfeeding=instance.breastfeeding,
            pregnant=instance.pregnant
            ).first()

        if recommended:
            instance.recommended = recommended
            instance.save(update_fields=['recommended'])


@receiver(post_save, sender=User)
def create_user_total_intake(sender, instance, created, **kwargs):
    if created: # User 객체가 처음 생성될 때만 실행
        for nutrient in Nutrient.objects.all():
            UserTotalIntake.objects.create(
                user=instance,
                nutrient=nutrient,
                dosage=0.0
            )
# admin.py
from django.contrib import admin
from .models import Nutrient, Synonym, Supplement, SupplementNutrient, RecommendedIntake, RecommendedNutrient

admin.site.register(Nutrient)
admin.site.register(Synonym)
admin.site.register(Supplement)
admin.site.register(SupplementNutrient)
admin.site.register(RecommendedIntake)
admin.site.register(RecommendedNutrient)
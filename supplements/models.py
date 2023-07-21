from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.name

class Synonym(models.Model):
    nutrient = models.ForeignKey(Nutrient, related_name='synonyms', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class NutrientBulk(models.Model):
    name = models.CharField(max_length=200)
    nutrients = models.ManyToManyField(Nutrient, through='NutrientDosage')

    def __str__(self):
        return self.name
    
class NutrientDosage(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    nutrientberk = models.ForeignKey(NutrientBulk, on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)

from django.db import models

# Create your models here.
class OCRResult(models.Model):
    text = models.TextField()
    supplement = models.ManyTOMAnyField('supplemnets.Supplement')

    def __str__(self):
        return self.text
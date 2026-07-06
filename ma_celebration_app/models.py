from django.db import models


class WeddingCelebration(models.Model):
    groom_name = models.CharField(max_length=120)
    bride_name = models.CharField(max_length=120)
    wedding_date = models.DateField()
    ceremony_time = models.TimeField(blank=True, null=True)
    church_name = models.CharField(max_length=150, default='Église')
    priest_name = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['wedding_date', 'ceremony_time']
        verbose_name = 'Célébration de mariage'
        verbose_name_plural = 'Célébrations de mariage'

    def __str__(self):
        return f"{self.groom_name} & {self.bride_name} - {self.wedding_date}"

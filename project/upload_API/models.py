from django.db import models

class BlockItem(models.Model):
    current_block = models.PositiveIntegerField()
    begin_row = models.PositiveIntegerField()
    end_row = models.PositiveIntegerField()
    begin_col =  models.PositiveIntegerField()
    end_col = models.PositiveIntegerField()
    data_string = models.CharField(max_length=100, blank=True)
    
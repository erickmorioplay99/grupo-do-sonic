from django.db import models

# Create your models here.
class product(models.Model):
    code = models.TextField(max_length=20, blank=False, null=False)
    nome = models.TextField(max_length=205, blank=False, null=False)
    description = models.TextField(max_length=500 ,blank=True, null=True)
    picture = models.ImageField(upload_to='products/', blank=True, null=True)
    qtt = models.IntegerField(blank=False, null=False)
    unity = models.TextField(max_length=3, blank=False, null=False) 
    price = models.DateTimeField(max_length=8, blank=False, null=False)

    def __str__(self): 
        return f' {self.code} - {self.nome}'
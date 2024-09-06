from django.db import models

class Users(models.Model):
    user = models.CharField(verbose_name="user", primary_key=True, max_length=50)
    
    class Meta():
        db_table = "users"


class Notes(models.Model):
    label = models.CharField(verbose_name="label", max_length=150)
    content = models.CharField(verbose_name="content", max_length=10000, blank=True, null=True, default="")
    user_id = models.ForeignKey(to=Users, verbose_name="user", max_length=32, on_delete=models.CASCADE)
    
    class Meta():
        db_table = 'notes'
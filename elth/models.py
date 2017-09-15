from django.db import models

# Create your models here.
from jsonfield import JSONField

class details(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	gender =  models.BooleanField(default=False) #True is Male, False is Female
	age = models.IntegerField(default = 18)

	class Meta:
		ordering = ('created',)
	
class questions_json(models.Model):
	questions = JSONField()
	q_no = models.IntegerField(default = 1)
	
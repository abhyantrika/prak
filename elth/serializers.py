from rest_framework import serializers
from elth.models import *

class detailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = details 
		fields = '__all__'

class questionSerializer(serializers.ModelSerializer):
	class Meta:
		model = questions_json
		fields = '__all__'  
 

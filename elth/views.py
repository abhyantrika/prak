from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elth.models import details,questions_json
from elth.serializers import detailsSerializer,questionSerializer
import itertools,json

@api_view(['POST','GET'])
def details_view(request):

	if request.method == 'GET':
		details_everyone = details.objects.all()
		serializer = detailsSerializer(details_everyone,many=True)
		return Response(serializer.data)

	if request.method == 'POST':
		serializer = detailsSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response("Congratulations! Registration Successful.", status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#For posting and viewing all questions of a particular track.
@api_view(['POST','GET'])
def questions_post(request):
	if request.method == 'POST':
		print(request.data)
		serializer = questionSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response("Bot created!!",status = status.HTTP_201_CREATED)
		return	Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	if request.method == 'GET':
		all_questions = questions_json.objects.all()
		serializer = questionSerializer(all_questions,many=True)
		return Response(serializer.data)


#For querying a particular question/instruction fromt the input track
@api_view(['POST','GET'])
def query_questions(request,q_no):
	if request.method == 'GET':
		required_question = questions_json.objects.filter(q_no = q_no)
		serializer = questionSerializer(required_question,many=True)
		return Response(serializer.data,status = status.HTTP_201_CREATED)		
	return	Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		

#Delete all current questions
@api_view(['GET'])
def delete(request):
	if request.method == 'GET':
		all_questions = questions_json.objects.all().delete()
		return Response("DONE",status = status.HTTP_201_CREATED)
	return	Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
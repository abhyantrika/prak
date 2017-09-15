from django.conf.urls import url,include
from elth import views

urlpatterns = [
	url(r'^details/$',views.details_view),
	url(r'^question/$',views.questions_post),
	#url(r'^query/$',views.query_questions),
	url(r'^delete/$',views.delete),
	url(r'^query/(?P<q_no>[0-9]+)/$', views.query_questions),
]
 

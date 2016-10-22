from django.conf.urls import url, include
from polls import views

app_name='polls'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^create_question/', views.create_question, name='create_question'),
    url(r'^(?P<question_id>[0-9]+)/add_choices/', views.add_choices, name='add_choices'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/result/$', views.result, name='result'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

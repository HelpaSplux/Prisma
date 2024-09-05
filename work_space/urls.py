from django.urls import path
from work_space import views

app_name = 'work_space'

urlpatterns = [
    path('', views.WorkSpaceView.as_view(), name='index'),
    path('create-file/', views.FileCreationFormView.as_view(), name='file-creation-form')
]

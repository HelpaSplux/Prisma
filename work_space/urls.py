from django.urls import path
from work_space import views

app_name = 'work_space'

urlpatterns = [
    path('', views.WorkSpaceView.as_view(), name='index'),
    path('create-file/', views.FileCreationFormView.as_view(), name='file-creation-form'),
    path('delete-file/', views.file_deletion_form_view, name='file-deletion-form'),
    path('open-file/', views.OpenedFileView.as_view(), name='opened-file'),
    path('save-file/', views.SaveChangesView.as_view(), name='save-file'),
    
]

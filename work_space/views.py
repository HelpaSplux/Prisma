from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from django.template.loader import render_to_string
from django.db.utils import IntegrityError

from work_space.forms import FileCreationForm
from .models import Notes, Users



class WorkSpaceView(TemplateView):
    template_name = 'work_space/work_space.html'
    
    # Add all notes for current session to context
    def get_context_data(self, **kwargs) -> dict:
        
        # Save session data and get session key
        session = self.request.session
        session.save()
        session_key = session.session_key
        
        # Add data to context
        context = super().get_context_data(**kwargs)
        context["files"] = Notes.objects.filter(user_id_id=session_key)
        return context
    


class FileCreationFormView(FormView):
    form_class = FileCreationForm
    

    def form_valid(self, form):
        # Save session data and get session key
        session = self.request.session
        session.save()
        session_key = session.session_key
        
        # Get 'label' field from form 
        label = form.cleaned_data["label"]
        
        # Create an object in Notes table if user with this session already exist in table Users
        # if it's not create a auser in table Users and try to create object in table Notes  
        try:
            if Notes.objects.filter(label=label, user_id_id=session_key).exists():
                response_data = {"message": "File with this label already exists."}
                return JsonResponse(data=response_data, status=200)
            
            Notes.objects.create(label=label, user_id_id=session_key)
        except IntegrityError:
            Users.objects.create(user=session_key)
            Notes.objects.create(label=label, user_id_id=session_key)
    
        # Create a context for 'render_to_string' function
        context = {
            "file": Notes.objects.filter(label=label, user_id_id=session_key).values('label')[0]["label"]
        }
        
        # Create response data and pass it to response
        new_file_button = render_to_string("work_space/new-button.html", context=context)  
        response_data = {
            "message":"File has been created successfuly.",
            "new_file": new_file_button
        }
        return JsonResponse(data=response_data, status=200) 

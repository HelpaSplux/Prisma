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
        
        # Creates a list with tuples.
        # Each tuple contain note's button id and note's lable
        notes = []
        db_notes = Notes.objects.filter(user_id_id=session_key)
        for note in db_notes:
            note_label = note.label
            note_button_id = note.label.replace(" ", "_") + "_button_id"
            notes.append((note_label, note_button_id))
        
        # Add data to context
        context = super().get_context_data(**kwargs)
        context["notes"] = notes
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
                response_data = {"message": "The file with this label already exists."}
                return JsonResponse(data=response_data, status=400)
            
            Notes.objects.create(label=label, user_id_id=session_key)
        except IntegrityError:
            Users.objects.create(user=session_key)
            Notes.objects.create(label=label, user_id_id=session_key)

        # Create response data and pass it to response
        response_data = {
            "message":"The file was successfully created.",
        }
        return JsonResponse(data=response_data, status=200) 
    
    
class OpenedFileView(TemplateView):
    template_name = "work_space/right_panel.html"

    def get_context_data(self, **kwargs) -> dict:
        session = self.request.session.session_key
        label = self.request.GET["label"]
        note = Notes.objects.filter(label=label, user_id_id=session).first()

        context = super().get_context_data(**kwargs)
        context["panel_id"] = note.label.replace(" ", "_") + "_panel_id"
        context["note"] = note
        return context
    
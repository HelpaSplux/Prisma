from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView, FormView, View

import logging

from work_space.forms import FileCreationForm
from .models import Notes, Users



logger = logging.getLogger(__name__)



class WorkSpaceView(TemplateView):
    template_name = 'work_space/work_space.html'
    
    # Add all notes for current session to context
    def get_context_data(self, **kwargs) -> dict:
        logger.info("Forming context data...")
        
        # Save session data and get session key
        session = self.request.session
        session.save()
        logger.debug(f"[WorkSpaceView] [COOKIES] [{self.request.COOKIES}]")
        logger.debug(f"[WorkSpaceView] [session_key] [{self.request.session.session_key}]")
        session_key = session.session_key
        
        # Creates a list with tuples.
        # Each tuple contain note's button id and note's lable
        logger.info("Attempting to get note from DB...")
        db_notes = Notes.objects.filter(user_id=session_key)
        logger.info("Complete.")
        
        logger.debug(f"[WorkSpaceView] [db_notes] [{db_notes}]")
        notes = []
        for note in db_notes:
            note_label = note.label
            note_button_id = note.label.replace(" ", "_") + "_button_id"
            notes.append((note_label, note_button_id))
        
        # Add data to context
        context = super().get_context_data(**kwargs)
        context["notes"] = notes
        
        logger.info("Complete.")
        return context
    
    


class FileCreationFormView(FormView):
    form_class = FileCreationForm

    def form_valid(self, form):
        logger.info("Form is valid")
        
        # Save session object
        session = self.request.session
        session.save()

        # Get session_key
        session_key = session.session_key
        logger.debug(f"session_key from request - {session_key}")
        
        # Get 'label' field from form 
        label = form.cleaned_data["label"]
        logger.debug(f"label variable from form's cleaned data - {label}")            
        
        user_exists = Users.objects.filter(user=session_key).exists()
        
        # Creates user if it's not exists
        if not user_exists:
            logger.info("Attempting to create a user...")
            Users.objects.create(user=session_key)
            logger.info("Complete.")
        
        # Returns an 400 response if it finds duplicate records 
        if user_exists and Notes.objects.filter(label=label, user_id=session_key).exists():
            logger.info("Failed to create a duplicate record.")
            logger.info("Sending error response...")
            response_data = {"message": "The file with this label already exists."}
            return JsonResponse(data=response_data, status=400)
        
        # Creates a record in DB
        logger.info("Attempting to create a record...")
        Notes.objects.create(label=label, user_id=session_key)
        logger.info("Complete.")
        
        # Create response data and pass it to response
        response_data = {
            "message":"The file was successfully created.",
        }
        
        logger.info("Sending response...")
        return JsonResponse(data=response_data, status=200) 
    
    
    
    
class OpenedFileView(TemplateView):
    template_name = "work_space/right_panel.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context == None:
            logger.info("Sending 404 error response...")
            return HttpResponseNotFound()
        
        logger.info("Sending response...")
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs) -> dict:
        logger.info("Forming context data...")
        
        session = self.request.session.session_key
        label = self.request.GET["label"]
        logger.debug(f"User - {session}")
        logger.debug(f"Note label - {label}")
        logger.debug(f"Request - {self.request}")
        
        logger.info("Attempting to get note from DB...")
        note = Notes.objects.filter(label=label, user_id=session).first()            
        logger.info("Complete.")
        
        context = super().get_context_data(**kwargs)
        try:
            context["panel_id"] = note.label.replace(" ", "_") + "_panel_id"
        except AttributeError:
            logger.warning("File not found.")
            return None
        
        context["note"] = note
        logger.debug(f"context['panel_id'] = {context['panel_id']}")
        logger.debug(f"context['note'] = {context['note']}")
        
        logger.info("Complete.")
        return context
    


def file_deletion_form_view(request):
    '''
    Handles deletion request:
        - if record exists - deletes it and returns success message.
        - if not exists - returns failure message
    '''
    
    session = request.session.session_key
    file_name = request.GET["label"]
    record = Notes.objects.filter(label=file_name, user_id=session)
    
    response_data = {"message": f"'{file_name}' was deleted successfully."}
    status_code = 200
    logger.debug(f"Query parameter 'label': {file_name}")

    if record.exists():
        record.delete()
    else:
        response_data["message"] = f"Failed to delete '{file_name}'"
        status_code = 400
            
    return JsonResponse(data=response_data, status=status_code)
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView, FormView

import logging

from work_space.forms import FileCreationForm, SaveChangesForm
from .models import Notes, Users



logger = logging.getLogger(__name__)



class WorkSpaceView(TemplateView):
    template_name = 'work_space/work_space.html'
    
    # Add all notes for current session to context
    def get_context_data(self, **kwargs) -> dict:
        logger.info("CONTEXT | Forming context data.")
        
        # Save session data and get session key
        logger.debug(f"REQUEST | Session key BEFORE session was triggered: {self.request.session.session_key}")
        
        
        session = self.request.session
        session.save()
        session_key = session.session_key
        
        
        logger.debug(f"REQUEST | Cookies: {self.request.COOKIES}")
        logger.debug(f"REQUEST | Session key AFTER session was triggered: {self.request.session.session_key}")
        
        # Creates a list with tuples.
        # Each tuple contain note's button id and lable
        logger.info("RECORD | Requesting record from DB.")
        
        
        db_notes = Notes.objects.filter(user_id=session_key)
        
        
        logger.info("RECORD | Record recived.")
        logger.debug(f"RECORD | Variable 'db_notes' contains: {db_notes}")
        
        
        notes = []
        for index, note in enumerate(db_notes):
            note_label = note.label
            file_id = index
            notes.append((note_label, file_id))
        
        # Add data to context
        context = super().get_context_data(**kwargs)
        context["notes"] = notes
        logger.info("CONTEXT | Context data is ready.")
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
    
    def form_invalid(self, form):
        response_data = {
            "message": "Server error."
        }
        
        return JsonResponse(data=response_data, status=500) 
    
    
    
class OpenedFileView(TemplateView):
    template_name = "work_space/right_panel.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context == None:
            logger.info("Sending 404 error response.")
            return HttpResponseNotFound()
        
        logger.info("Sending response.")
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs) -> dict:
        logger.info("Forming context data.")
        
        
        session = self.request.session.session_key
        label = self.request.GET["label"]
        file_id = self.request.GET["file_id"]
        
        
        logger.debug(f"User - {session}")
        logger.debug(f"Note label - {label}")
        logger.debug(f"Request - {self.request}")
        logger.info("Attempting to get note from DB.")
               
               
        context = super().get_context_data(**kwargs)
        note = Notes.objects.filter(label=label, user_id=session)
        if note.exists():
            context["note"] = note.first()
            context["file_id"] = file_id

        logger.debug(f"context['file_id'] = {context['file_id']}")
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


class SaveChangesView(FormView):
    form_class = SaveChangesForm
    
    def form_valid(self, form):
        logger.info("Form is valid")

        response_data = dict()
        
        # Get session_key
        old_label = form.cleaned_data.get("old_label")
        new_label = form.cleaned_data.get("new_label")
        content = form.cleaned_data.get("content")
        session_key = self.request.session.session_key


        logger.debug(f"session_key from request - {session_key}")
        
        
        if not session_key: 
            return JsonResponse(data={"message": "Not authorized user."}, status=400)
        

        record = Notes.objects.filter(label=old_label, user_id=session_key)
        logger.debug(f"Variable 'record' is: {record}")
        
        if record.exists() and new_label: 
            record.update(label=new_label, content=content)
            response_data["message"] = "Changes saved."
            return JsonResponse(data=response_data, status=200)
        
        response_data["message"] = "Error. Failed to save."
        return JsonResponse(data=response_data, status=400) 
    
    
    def form_invalid(self, form):
        response_data = {"message": "Error. Title can't be blank."}
        return JsonResponse(data=response_data, status=400)
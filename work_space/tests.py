from django.test import TestCase
from django.urls import reverse
import logging

from .models import Notes, Users

class WorkSpaceViewTests(TestCase):
    
    def test_1(self):
        '''
        User alredy exists in DB and have some notes in table 'notes'.
        
        Table 'notes' contains other users notes
        
        Table 'users' contains other user
        '''
        logging.basicConfig(level=logging.INFO, format="[WorkSpaceViewTests] [%(funcName)s] [%(asctime)s] [%(levelname)s] %(message)s")
        
        logging.info("Start testing.")
        logging.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logging.debug(f"[Cookies data type] [{type(self.client.cookies)}]")
        logging.debug(f"[Session key] [{self.client.session.session_key}]")
        logging.debug(f"[Interaction with session was occured]")
        
        # Get session key
        session = self.client.session.session_key
 
        logging.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logging.debug(f"[Session key] [{session}]")
        
        # Create users in table 'users'
        Users.objects.bulk_create(
            [
                Users(user=session),
                Users(user="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logging.info("Two users was added into a table 'users'")
        
        # Create notes in table 'notes'
        db_notes = Notes.objects.bulk_create(
            [
                Notes(label="Parot", content="Just a tiny parot", user_id_id=session),
                Notes(label="Smoll", content="So smoll", user_id_id=session),
                Notes(label="The spirit city", content="There are only spirits", user_id_id="7e608yzjayddm5mn5raof6feahyggb4w"),
                Notes(label="Power bank", content="Power", user_id_id="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logging.info("Four notes was added into a table 'notes'")
        
        # Fill variable notes with note lable and button id
        notes = []
        for note in db_notes:
            if note.user_id_id == session:
                label = note.label
                button_id = f"{label}_button_id"
                notes.append((label, button_id))
        
        logging.info("Sending request...")
        
        # Send request
        response = self.client.get(reverse("work-space:index")) 
        
        logging.info("The response was recived.")
        logging.debug(f"[Session key] [{session}]")
        logging.debug(f"[notes] [{notes}]")
        logging.debug(f"[response] [{response}]")
        logging.debug(f"[response.context['notes']] [{response.context['notes']}]")
        logging.info("Cheking values...")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"], notes)
        
        logging.info("All checks have been completed successfuly.")
        logging.info("End testing.")
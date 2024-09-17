from django.test import TestCase
from django.urls import reverse

import logging

from .models import Notes, Users
from .test_utils import create_records


logger = logging.getLogger(__name__)



class WorkSpaceViewTests(TestCase):
    
    def test_existing_user(self):
        '''
        User alredy exists in DB and have some notes in table 'notes'.
        
        Table 'notes' contains other users notes
        
        Table 'users' contains other user
        '''
        logger.info("Start testing.")
        logger.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logger.debug(f"[Cookies data type] [{type(self.client.cookies)}]")
        logger.debug(f"[Session key] [{self.client.session.session_key}]")
        logger.debug(f"[Interaction with session was occured]")
        
        # Get session key
        session = self.client.session.session_key
 
        logger.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logger.debug(f"[Session key] [{session}]")
        
        # Create users in table 'users'
        Users.objects.bulk_create(
            [
                Users(user=session),
                Users(user="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logger.info("Two users was added into a table 'users'")
        
        # Create notes in table 'notes'
        Notes.objects.bulk_create(
            [
                Notes(label="Parot", content="Just a tiny parot", user_id=session),
                Notes(label="Smoll", content="So smoll", user_id=session),
                Notes(label="The spirit city", content="There are only spirits", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
                Notes(label="Power bank", content="Power", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logger.info("Four notes was added into a table 'notes'")
        logger.info("Sending request...")
        
        # Send request
        response = self.client.get(reverse("work-space:index")) 
        
        logger.info("The response was recived.")
        logger.debug(f"[Session key] [{session}]")
        logger.debug(f"[response] [{response}]")
        logger.debug(f"[response.context['notes']] [{response.context['notes']}]")
        logger.info("Cheking values...")
        
        self.assertEqual(response.status_code, 200)
        response_notes = response.context["notes"]
        self.assertIsInstance(response_notes, list)
        for note in response_notes:
            label = note[0]
            button_id = note[1]
            self.assertIsInstance(note, tuple)
            self.assertIsInstance(label, str)
            self.assertIsInstance(button_id, str)
            self.assertIn("_button_id", button_id)
            self.assertIn(label, button_id)
            
            
        
        logger.info("All checks have been completed successfuly.")
        logger.info("End testing.")
        
    def test_not_existing_user(self):
        '''
        User does not exists in DB and have some notes in table 'notes'.
        
        Table 'notes' contains other users notes
        
        Table 'users' contains other user
        '''
        
        logger.info("Start testing.")
        logger.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logger.debug(f"[Cookies data type] [{type(self.client.cookies)}]")
 
        logger.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        
        # Create users in table 'users'
        Users.objects.bulk_create(
            [
                Users(user="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logger.info("User was added into a table 'users'")
        
        # Create notes in table 'notes'
        Notes.objects.bulk_create(
            [
                Notes(label="The spirit city", content="There are only spirits", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
                Notes(label="Power bank", content="Power", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
            ]
        )
        
        logger.info("Two notes was added into a table 'notes'")
        logger.info("Sending request...")
        
        # Send request
        response = self.client.get(reverse("work-space:index")) 
        
        logger.info("The response was recived.")
        logger.debug(f"[response] [{response}]")
        logger.debug(f"[response.context['notes']] [{response.context['notes']}]")
        logger.info("Cheking values...")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"], [])
        self.assertIn("sessionid", response.cookies)
        
        logger.info("All checks have been completed successfuly.")
        logger.info("End testing.")
        
        

class FileCreationFormViewTests(TestCase):
    
    def test_existing_user_1(self):
        '''
        User exists in database and don't have any records in table 'notes'.
    
        All tables are empty.
        '''    

        logger.info("Start testing.")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Creating records in DB
        logger.info("Creating records in DB...")
        create_records(user=Users(user=session), empty_tables=True)
        logger.info("Complete.")
        
        
        form_data = {
            "label": "Wonderful note",
        }
        
        
        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        
        # Get all records from tables "users" & "notes"
        logger.info("Making requests to DB...")
        users = Users.objects.all()
        notes = Notes.objects.all()
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Tabel users - {users}")
        logger.debug(f"    user - {users.first().user}")
        logger.debug(f"Table notes - {notes}")
        logger.debug(f"    label - {notes.first().label}")
        logger.debug(f"    content- {notes.first().content}")
        logger.debug(f"    user_id - {notes.first().user_id}")
        
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(users.first().user, session)
        self.assertEqual(notes.first().user_id, session)
        self.assertEqual(notes.first().label, form_data["label"])
        self.assertEqual(notes.first().content, "")
        logger.info("All checks have been completed successfuly.")
        
        
        logger.info("End testing.")
        
    def test_existing_user_2(self):
        '''
        User exists in database and don't have any records in table 'notes'.
    
        All tabels filled with other users data.
        '''    
        logger.info("Start testing.")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Creating records in DB
        logger.info("Creating records in DB...")
        create_records(user=Users(user=session))
        logger.info("Complete.")
        
        
        form_data = {
            "label": "Wonderful note",
        }
        
        
        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        
        # Get all records from tables "users" & "notes"
        logger.info("Making requests to DB...")
        user = Users.objects.filter(user=session)
        notes = Notes.objects.filter(user=session)
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Current user - {user}")
        logger.debug(f"Current user notes - {notes}")
        logger.debug(f"    label - {notes.first().label}")
        logger.debug(f"    content- {notes.first().content}")
        logger.debug(f"    user_id - {notes.first().user_id}")
        
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user), 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(user.first().user, session)
        self.assertEqual(notes.first().user_id, session)
        self.assertEqual(notes.first().label, form_data["label"])
        self.assertEqual(notes.first().content, "")
        logger.info("All checks have been completed successfuly.")
        
        
        logger.info("End testing.")
            
    def test_existing_user_3(self):
        '''
        User exists in database and do have some records in table 'notes'
        
        All tabels filled with other users data.
        '''    
        logger.info("Start testing.")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Creating records in DB
        logger.info("Creating records in DB...")
        create_records(
            user=Users(user=session), 
            note=Notes(label="label", content="content", user_id=session)
        )
        logger.info("Complete.")
        
        
        form_data = {
            "label": "Wonderful note",
        }
        
        
        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        
        # Get all records from tables "users" & "notes"
        logger.info("Making requests to DB...")
        user = Users.objects.filter(user=session)
        notes = Notes.objects.filter(user=session)
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Current user - {user}")
        logger.debug(f"Current user notes - {notes}")
        
        for note in notes:
            logger.debug(f"Note - {note}")
            logger.debug(f"    label - {note.label}")
            logger.debug(f"    content- {note.content}")
            logger.debug(f"    user_id - {note.user_id}")
        
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user), 1)
        self.assertEqual(len(notes), 2)
        self.assertEqual(user.first().user, session)
        
        for note in notes:
            self.assertEqual(note.user_id, session)
            
            if note.label != "label":
                self.assertEqual(note.label, form_data["label"])
                self.assertEqual(note.content, "")
        logger.info("All checks have been completed successfuly.")
        
        
        logger.info("End testing.")
        
    def test_existing_user_4(self):
        '''
        User exists in database and trying to create a duplicate record in table 'notes'
    
        All tabels filled with other users data.
        '''    
        logger.info("Start testing.")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Creating records in DB
        logger.info("Creating records in DB...")
        create_records(
            user=Users(user=session), 
            note=Notes(label="Wonderful note", content="", user_id=session)
        )
        logger.info("Complete.")
        
        
        form_data = {
            "label": "Wonderful note",
        }
        
        
        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        
        # Get all records from tables "users" & "notes"
        logger.info("Making requests to DB...")
        user = Users.objects.filter(user=session)
        notes = Notes.objects.filter(user=session)
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Current user - {user}")
        logger.debug(f"Current user notes - {notes}")
        
        for note in notes:
            logger.debug(f"Note - {note}")
            logger.debug(f"    label - {note.label}")
            logger.debug(f"    content- {note.content}")
            logger.debug(f"    user_id - {note.user_id}")
        
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"message": "The file with this label already exists."}')
        self.assertEqual(len(user), 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(user.first().user, session)
    
        logger.info("All checks have been completed successfuly.")
        
        
        logger.info("End testing.")
        
        
    def test_not_existing_user_no_records(self):
        '''
        User does not exist in database and trying to create a record in table 'notes'.
        
        All tables are empty.
        '''    
        logger.info("Start testing.")
        
        form_data = {
            "label": "Wonderful note",
        }
        
        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Get all records from tables "users" & "notes"
        logger.info("Making requests to DB...")
        users = Users.objects.all()
        notes = Notes.objects.all()
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Tabel users - {users}")
        logger.debug(f"    user - {users.first().user}")
        logger.debug(f"Table notes - {notes}")
        logger.debug(f"    label - {notes.first().label}")
        logger.debug(f"    content- {notes.first().content}")
        logger.debug(f"    user_id - {notes.first().user_id}")
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(users.first().user, session)
        self.assertEqual(notes.first().user_id, session)
        self.assertEqual(notes.first().label, form_data["label"])
        self.assertEqual(notes.first().content, "")
        logger.info("All checks have been completed successfuly.")
        
        logger.info("End testing.")
         
    def test_not_existing_user_some_records(self):
        '''
        User does not exist in database and trying to create a record in table 'notes'.
        
        All tables are have some data from other users.
        '''    
        
        logger.info("Start testing.")
        
        # Creating records in DB
        logger.info("Creating records in DB...")
        create_records()
        logger.info("Complete.")
        
        form_data = {
            "label": "Wonderful note",
        }

        # Making request
        logger.info("Sending request...")
        response = self.client.post(reverse("work-space:file-creation-form"), data=form_data) 
        logger.info("Completed.")
        logger.debug(f"Response - {response}")
        
        # Get session key
        session = self.client.session.session_key
        logger.debug(f"Session key from Session object - {session}")
        
        # Get all records of current user from tables "users" & "notes"
        logger.info("Attempting to get records of current user from DB...")
        users = Users.objects.filter(user=session)
        notes = Notes.objects.filter(user_id=session)
        logger.info("Completed.")
        
        # Debug table info
        logger.debug(f"Tabel users - {users}")
        logger.debug(f"    user - {users.first().user}")
        logger.debug(f"Table notes - {notes}")
        logger.debug(f"    user_id - {notes.first().user_id}")
        logger.debug(f"    label - {notes.first().label}")
        logger.debug(f"    content - {notes.first().content}")
        
        # Making checks
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(users.first().user, session)
        self.assertEqual(notes.first().user_id, session)
        self.assertEqual(notes.first().label, form_data["label"])
        self.assertEqual(notes.first().content, "")
        logger.info("All checks have been completed successfuly.")
        
        logger.info("End testing.")
        


class OpenedFileViewTests(TestCase):
    
    def test_existing_file(self): 
        '''
        User requesting his existing note  
        '''
        logger.info("Start testing.")
        
        session = self.client.session.session_key
        create_records(
            user=Users(user=session),
            note=Notes(label="Wonderful note", content="Wonderful content", user_id=session)
        )
        
        
        logger.info("Sending request...")
        response = self.client.get(reverse("work-space:opened-file"), {"label": "Wonderful note"})
        logger.info("Complete.")
        
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'class="bottom_right_panel" id="Wonderful_note_panel_id"')
        self.assertContains(response, 'Wonderful note')
        self.assertContains(response, 'Wonderful content')
        logger.info("All checks have been completed successfuly.")
        
        logger.info("End testing.")
    
    def test_not_existing_file(self):
        '''
        User requesting not existing note
        '''
        logger.info("Start testing.")

        logger.info("Sending request...")
        response = self.client.get(reverse("work-space:opened-file"), {"label": "Wonderful note"})
        logger.info("Complete.")
        
        logger.info("Checking the values...")
        self.assertEqual(response.status_code, 404)

        logger.info("All checks have been completed successfuly.")
        
        logger.info("End testing.")
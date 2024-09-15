from django.test import TestCase
from django.urls import reverse

import logging

from .models import Notes, Users


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
        logger.debug(f"[Session key] [{self.client.session.session_key}]")
        logger.debug(f"[Interaction with session was occured]")
        
        # Get session key
        session = self.client.session.session_key
 
        logger.debug(f"[Cookies] [{self.client.cookies or '...'}]")
        logger.debug(f"[Session key] [{session}]")
        
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
        logger.debug(f"[Session key] [{session}]")
        logger.debug(f"[response] [{response}]")
        logger.debug(f"[response.context['notes']] [{response.context['notes']}]")
        logger.info("Cheking values...")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"], [])
        
        logger.info("All checks have been completed successfuly.")
        logger.info("End testing.")
        
        

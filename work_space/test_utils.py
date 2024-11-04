from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException
from psycopg2.errors import UniqueViolation

import time
import logging

from .models import Notes, Users




logger = logging.getLogger(__name__)

class SeleniumTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)    
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.close()
        return super().tearDownClass()

    def go_to_the_site(self) -> None:
        # Adding sessionid in cookies
        url = self.live_server_url + reverse("work-space:index")
        session = self.client.session.session_key
        logger.info(f"Requesting {url}.")
        self.selenium.get(url)
        self.selenium.add_cookie({"name": "sessionid", "value": session,})
        
        # Refreshing the page to apply cookie changes 
        logger.info(f"Refreshing page.")
        self.selenium.refresh()
        time.sleep(1)    
        return

    
    def get_current_file(self) -> dict[str: object]:
        panel = self.selenium.find_element(By.XPATH, "/html/body/div[2]/div[@style='display: block;']")
        
        current_file = dict(
            panel = panel,
            title_field = panel.find_element(By.CLASS_NAME, "label_field"),
            content_field = panel.find_element(By.CLASS_NAME, "content_field"),
            close_button = panel.find_element(By.CLASS_NAME, "close_file_button"),
            delete_button = panel.find_element(By.CLASS_NAME, "delete_file_button"),
            left_button= self.selenium.find_element(By.CLASS_NAME, "file_button_active"),
            top_button = self.selenium.find_element(By.CLASS_NAME, "tab_button_active"),
        )
        return current_file
    

    def _find_left_buttons(self) -> list[object]:
        button_class = "file_button"
        
        buttons = self.selenium.find_elements(By.CLASS_NAME, button_class)
        logger.debug(f"Found {len(buttons)} buttons.")
        logger.info("File opening.")
        
        return buttons
    
    
    def _find_top_buttons(self) -> list[object]:
        tab_class = "tab_button"
        tabs = self.selenium.find_elements(By.CLASS_NAME, tab_class)
        return tabs
    
    
    def create_file(self, input_data: int | str) -> None:
        logger.info("Createing a file.")
        create_button_class = "create_button"
        input_class = "file-name-input"
        submit_id = "file-creation-form-submit"

        time.sleep(1)
        create_button = self.selenium.find_element(By.CLASS_NAME, create_button_class)
        create_button.click()
    
        time.sleep(1)
        input_field = self.selenium.find_element(By.CLASS_NAME, input_class)
        input_field.clear()   
        input_field.send_keys(str(input_data))
    
        submit_button = self.selenium.find_element(By.ID, submit_id)
        submit_button.click()        
        
        return
    

    def open_file(self, file_name: int) -> None:
        """Clicks on selected left button"""
        buttons = self._find_left_buttons()
        
        target_button = buttons[file_name]
        target_button.click()
        return
    
    
    def open_files(self) -> None:
        """Clicks on all left buttons"""
        buttons = self._find_left_buttons()
        for button in buttons:
            button.click()
        
        return
        
    
    def open_tab(self, tab: int) -> None:
        tabs = self._find_top_buttons()
        tabs[tab].click()
        return
        
    
    def delete_file(self, deleted_file: dict[str: object]) -> None:
        """Deletes current file"""
        deleted_file["delete_button"].click()
        time.sleep(1.5)
        
        confirmation_button = self.selenium.find_element(By.ID, "file-deletion-form-delete")
        confirmation_button.click()    
        return
    
    
    def close_file(self, closable_file: dict[str: object]) -> None:
        # Close current file
        closable_file["close_button"].click()
        return




    def assertCreated(self, file_name: int | str):
        left_buttons = self._find_left_buttons()
        left_buttons = [button.text for button in left_buttons]
        
        self.assertIn(str(file_name), left_buttons)
        return

        
    def assertOpenedTab(self, opened_file: dict[str: object]):
        tabs = tabs = self._find_top_buttons()
        last_tab = tabs[-1]
        current_tab = opened_file["top_button"]
        
        self.assertEqual(last_tab, current_tab)
        return
    
    
    def assertDeleted(self, deleted_file: dict[str: object]) -> None:
        with self.assertRaises(StaleElementReferenceException):
            deleted_file["left_button"].get_attribute("id")

        with self.assertRaises(StaleElementReferenceException):
            deleted_file["top_button"].get_attribute("id")

        with self.assertRaises(StaleElementReferenceException):
            deleted_file["title_field"].get_attribute("id")
        return
    
    
    def assertPrediction(self, prediction: int | str, opened_file: dict[str: object]) -> None:
        self.assertIn(str(prediction), opened_file["title_field"].text)
        self.assertIn(str(prediction), opened_file["left_button"].text)
        self.assertIn(str(prediction), opened_file["top_button"].text)
        return
    
    
    def assertHidden(self, suggested_file: dict[str: object]) -> None:
        self.assertEqual(suggested_file["left_button"].get_attribute("class"), "file_button")
        self.assertEqual(suggested_file["top_button"].get_attribute("class"), "tab_button")
        self.assertEqual(suggested_file["top_button"].get_attribute("style"), "display: none;")
        self.assertEqual(suggested_file["panel"].get_attribute("style"), "display: none;")
        return


            
class DBImage():
    '''
    Creates database image and allows you to create DB records based on this image.
    '''
    
    def __init__(self):
        self.users = []
        self.notes = []
        return
    
    @staticmethod
    def _create_note_models(self, records: int, user_id: str | int = None) -> None:
        """
        Creates `Notes` objects and save them to `self.notes`.
        
        - `records` - Number of records to be created.
        - `user_id` - Describes user in table `users`. It can be session key or something else.
        """
        
        for note_number in range(records):
            note = Notes(label=note_number, content=note_number, user_id=user_id)
            self.notes.append(note)
            logger.debug(f"Note {note_number} created.")
        return
    
    
    def add_other_users(self, count: int, records: int) -> None:
        """
        Creates models for other users and seve them.
        
        - `count` - number of users to be created.
        - `records` - number of records to be created for each user.
        """
        
        logger.info(f"Createing models for other users.")
        logger.debug(f"Input arguments: count = {count}, records = {records}.")        
        if count:
            for user_number in range(count):
                # Cretaes user
                logger.debug(f"Creating user {user_number}.")
                user = Users(user=user_number)
                self.users.append(user)
                
                if records:
                    # Creates notes for user    
                    logger.debug(f"Creating notes for user {user_number}.")
                    self._create_note_models(self, records, user_number)
        return


    def add_tested_user(self, test_object: object, records: int) -> None:
        """
        Creates models for tested user and seve them.
        
        - `test_object` - `self` object.  
        - `records` - number of records to be created for tested user.
        """
        
        logger.info(f"Createing models for tested user.")
        
        # Creating user
        session = test_object.client.session.session_key
        user = Users(user=session)
        self.users.append(user)
        
        # Creating notes for user
        if records:    
            logger.debug(f"Creating notes for user {session}.")
            self._create_note_models(self, records, session)
        return


    def create_records(self) -> None:
        """
        Uses previously created models for creating a records in the database.
        """
        
        # Create records in table 'users'
        try:
            logger.info("Creating records in table 'users'.")
            Users.objects.bulk_create(self.users)
        except UniqueViolation:
            logger.info("Failed to cretae a user.")
            logger.warning("This user already exists")
            
        # Create records in table 'notes'
        try:
            logger.info("Creating records in table 'notes'.")
            Notes.objects.bulk_create(self.notes)
        except UniqueViolation:
            logger.info("Failed to cretae a note.")
            logger.warning("This note already exists")
        return


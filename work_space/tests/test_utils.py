from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException
from psycopg2.errors import UniqueViolation

import time
import logging

from ..models import Notes, Users




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
        """Sets a cookie and goes to the site"""
        
        # Reqsting url
        url = self.live_server_url + reverse("work-space:index")
        logger.info(f"Requesting {url}.")
        self.selenium.get(url)
        
        # Adding sessionid in cookies
        session = self.client.session.session_key
        self.selenium.add_cookie({"name": "sessionid", "value": session})
        
        # Refreshing the page to apply cookie changes 
        logger.info(f"Refreshing page.")
        self.selenium.refresh()
        time.sleep(1)    
        return

    
    def get_current_file(self) -> dict[str: object]:
        """Returns currently opened file."""
        
        logger.info("Getting current file.")
        
        # Getting file components
        panel = self.selenium.find_element(By.CLASS_NAME, "bottom_right_panel.active")
        left_button = self.selenium.find_element(By.CLASS_NAME, "file_button.active")
        top_button = self.selenium.find_element(By.CLASS_NAME, "tab_button.active")
        
        # Put the components into a dict
        current_file = dict(
            left_button = left_button,
            top_button = top_button,
            panel = panel,
            
            title_field = panel.find_element(By.CLASS_NAME, "label_field"),
            content_field = panel.find_element(By.CLASS_NAME, "content_field"),
            close_button = panel.find_element(By.CLASS_NAME, "close-button"),
            dropdown_menu = panel.find_element(By.CLASS_NAME, "dropdown"),
            delete_button = panel.find_element(By.CLASS_NAME, "delete-button"),
        )

        return current_file
    

    def _find_left_buttons(self) -> list[object]:
        """Returns all left buttons in the template."""
        
        logger.info("Finding left buttons.")
        button_class = "file_button"
        
        buttons = self.selenium.find_elements(By.CLASS_NAME, button_class)

        logger.debug(f"Found {len(buttons)} buttons.")
        
        return buttons
    
    
    def _find_top_buttons(self) -> list[object]:
        """Returns all top buttons in the template."""
        
        logger.info("Finding top buttons.")
        tab_class = "tab_button"
        tabs = self.selenium.find_elements(By.CLASS_NAME, tab_class)
        return tabs
    
    
    def create_file(self, file_name: int | str) -> None:
        """Created a file with chosen file name."""
        
        logger.info("Createing a file.")
        create_button_class = "create_button"
        input_class = "file-name-input"
        submit_id = "file-creation-form-submit"

        # Clicking on create button
        time.sleep(1)
        create_button = self.selenium.find_element(By.CLASS_NAME, create_button_class)
        create_button.click()

        # Filling input field
        time.sleep(1)
        input_field = self.selenium.find_element(By.CLASS_NAME, input_class)
        input_field.clear()   
        input_field.send_keys(str(file_name))

        # Clicking on submit button
        submit_button = self.selenium.find_element(By.ID, submit_id)
        submit_button.click()            

        
        return
    

    def open_file(self, file_name: int) -> None:
        """Presses the selected left button"""
        logger.info(f"Opening file - '{file_name}'")
        
        buttons = self._find_left_buttons()
        
        target_button = buttons[file_name]
        target_button.click()
        return
    
    
    def open_files(self) -> None:
        """Clicks on all the left buttons."""
        
        logger.info("Opening all files.")
        buttons = self._find_left_buttons()
        for button in buttons:
            button.click()
        
        return
        
    
    def open_tab(self, tab_number: int) -> None:
        """Opens chosen tab."""
        
        logger.info(f"Opening {tab_number} tab")
        tabs = self._find_top_buttons()
        tabs[tab_number].click()
        return
        
        
    def _open_dropdown_menu(self):
        current_file = self.get_current_file
        dropdown_menu = current_file["dropdown_menu"]
        dropdown_menu.click()
        return
        
    
    def delete_file(self, deletable_file: dict[str: object]) -> None:
        """
        Deletes the current file
        
        - `deletable_file` - Return of `get_current_file` method.
        """
        logger.info("Deleting current file.")
        
        # Clicking on delete button
        deletable_file["dropdown_menu"].click()
        time.sleep(0.3)
        deletable_file["delete_button"].click()
        time.sleep(1.5)
        
        # Clicking on delete confirmation button 
        confirmation_button = self.selenium.find_element(By.ID, "file-deletion-form-delete")
        confirmation_button.click()    
        return
    
    
    def close_file(self, closable_file: dict[str: object]) -> None:
        """
        Closes the current file.
        
        - `closable_file` - Return of `get_current_file` method.
        """
        
        logger.info("Closing current file.")
        closable_file["close_button"].click()
        return




    def assertCreated(self, file_name: int | str) -> None:
        """Checks whether the left button of the created file is displayed in the file list."""
        
        left_buttons = self._find_left_buttons()
        left_buttons = [button.text for button in left_buttons]
        
        logger.info("Validating data")
        
        # Checks if file name contains in left buttons
        self.assertIn(str(file_name), left_buttons)
        return

        
    def assertOpenedTab(self, opened_file: dict[str: object]) -> None:
        """
        Checks if the opened tab is at the end of the tab list.
        
        - `opened_file` - Return of `get_current_file` method.
        """
        tabs = self._find_top_buttons()
        last_tab = tabs[-1]
        current_tab = opened_file["top_button"]
        
        logger.info("Validating data")
        
        # Checks if current tab is last tab.
        self.assertEqual(last_tab, current_tab)
        return
    
    
    def assertDeleted(self, file: dict[str: object]) -> None:
        """
        Checks if `file` is deleted.
        
        - `file` - Return of `get_current_file` method.
        """
        
        exception_class = StaleElementReferenceException
        logger.info("Validating data")
        
        # Checks if the file components exists
        self.assertRaises(exception_class, file["left_button"].click)
        self.assertRaises(exception_class, file["top_button"].click)
        self.assertRaises(exception_class, file["title_field"].click)

        return
    
    
    def assertPrediction(self, prediction: int | str, opened_file: dict[str: object]) -> None:
        """
        Checks if the prediction and the opened file is match.
        
        - `prediction` - Predicted file name
        - `opened_file` - The file that is currently open.
        """
        logger.info("Validating data")
        
        # Checks if prediction in the file components
        self.assertIn(str(prediction), opened_file["title_field"].text)
        self.assertIn(str(prediction), opened_file["left_button"].text)
        self.assertIn(str(prediction), opened_file["top_button"].text)
        return
    
    
    def assertClosed(self, suggested_file: dict[str: object]) -> None:
        """
        Checks if `suggested_file` is closed.
        
        `suggested_file` - Return of `get_current_file` method.
        """
        logger.info("Validating data")
        logger.debug(f"Left button class is: '{suggested_file['left_button'].get_attribute('class')}'.")
        
        # Checks if the file components are changed properly 
        self.assertEqual(suggested_file["left_button"].get_attribute("class"), "file_button")
        self.assertIn("hidden", suggested_file["top_button"].get_attribute("class"))
        self.assertIn("tab_button", suggested_file["top_button"].get_attribute("class"))
        self.assertEqual(suggested_file["panel"].get_attribute("class"), "bottom_right_panel")
        return


            
class DBImage():
    '''
    Creates database image and allows you to create DB records based on this image.
    '''
    
    def __init__(self) -> None:
        logger.info("Building database image.")
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
        
        logger.info("Creating models.")
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
        logger.info("Adding other users in database image.")
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
        
        logger.info("Adding tested user in database image.")
        
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
            logger.warning("Failed to cretae a user. This user already exists.")
            
        # Create records in table 'notes'
        try:
            logger.info("Creating records in table 'notes'.")
            Notes.objects.bulk_create(self.notes)
        except UniqueViolation:
            logger.warning("Failed to cretae a note. This note already exists.")
        return


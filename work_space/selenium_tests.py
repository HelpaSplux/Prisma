
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

import logging
import time

from .models import Notes, Users
from .test_utils import create_records



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
    
    
    
    
class TEST_CREATE_FILES_AND_ONE_DUPLICATE(SeleniumTest):
    def test(self):
        logger.info("TEST | Testing begins.")
        
        url = self.live_server_url + reverse("work-space:index")
        
        logger.info(f"REQUEST | Requesting {url}.")
        self.selenium.get(url)
        logger.info("REQUEST | Response recived.")
        time.sleep(1)
        
        create_button = "/html/body/div[2]/div/button"
        file_name_input = "/html/body/div[3]/form/div/input"
        submit_button = "//*[@id='file-creation-form-submit']"
        files = [
            "AMD",
            "Nvidia",
            "Intel",
            "Intel",
        ]
        
        # Create files
        logger.info("FILES | Createing files.")
        for file in files:
            self.selenium.find_element(By.XPATH, create_button).click()
            time.sleep(1)
            
            form_input = self.selenium.find_element(By.XPATH, file_name_input)
            form_input.clear()
            form_input.send_keys(file)
            time.sleep(1)
            
            self.selenium.find_element(By.XPATH, submit_button).click()
            time.sleep(3)
        logger.info("FILES | Files created.")
        
        left_buttons_elemnts = self.selenium.find_elements(By.CLASS_NAME, "file_button")
        left_buttons = [button.text for button in left_buttons_elemnts]
        
        logger.info("TEST | Checking values.")
        self.assertEqual(len(left_buttons), 3)
        self.assertIn("AMD", left_buttons)
        self.assertIn("Nvidia", left_buttons)
        self.assertIn("Intel", left_buttons)
        logger.info("TEST | Checking completed.")
        logger.info("TEST | Testing completed.")
    
    
class TEST_OPEN_FILES(SeleniumTest):
    def test(self):
        logger.info("TEST | Testing begins.")
        target_url = self.live_server_url + reverse("work-space:index")
        
        # Creates user object
        user_info = dict(user=self.client.session.session_key)
        user = Users(**user_info)
        
        # Creates list of dict objects representing note records
        note_records = [
            dict(
                label="Vacuum",
                content="Almost nothing",
                user_id=user_info["user"],
            ),
            dict(
                label="Water",
                content="H₂O",
                user_id=user_info["user"],
            ),
            dict(
                label="Bronze",
                content="Copper and tin",
                user_id=user_info["user"],
            ),
        ]
        
        # Creates some random records and current user
        create_records(user=user)
        
        # Creates note records for current user
        for record_info in note_records:
            note = Notes(**record_info)
            create_records(note=note, only_arguments=True)

        # Setting sessionid in cookies
        print(f"REQUEST | Requesting {target_url}")
        self.selenium.get(target_url)
        self.selenium.add_cookie({
            "name": "sessionid",
            "value": user_info["user"],
        })
        print("REQUEST | Response recived.")
        
        # Refreshing the page to apply cookie changes 
        logger.info(f"REQUEST | Refreshing page.")
        self.selenium.refresh()
        logger.info("REQUEST | Page refreshed.")
        time.sleep(1)
        
        # This variable exists for debug logging
        user_info = self.client.session.session_key
        print(f"[USER | user_info = {user_info}]")

        
        # Finds all left buttons
        buttons = self.selenium.find_elements(By.CLASS_NAME, "file_button")
        print(f"[INFO] Found {len(buttons)} buttons.")
        
        # Clicks on left buttons and validate file components
        for button in buttons:
            print(f"[INFO] Clicking on button '{button.get_attribute('id')}'.")
            button.click()
            file_title = button.text
            
            
            # Checks if clicked button state has changed to active
            active_buttons = self.selenium.find_elements(By.CLASS_NAME, "file_button_active")
            self.assertEqual(len(active_buttons), 1)
            
            active_button = active_buttons[-1].text
            self.assertEqual(file_title, active_button)
            
            
            # Checks whether the state of the top button has been changed to active and added to the end of the list
            active_top_buttons = self.selenium.find_elements(By.CLASS_NAME, "tab_button_active")
            self.assertEqual(len(active_top_buttons), 1)
            
            last_top_button = self.selenium.find_elements(By.CLASS_NAME, "tab_button")[-1].text
            active_top_button = active_top_buttons[-1].text
            self.assertEqual(file_title, last_top_button)
            self.assertEqual(file_title, active_top_button)
            
            # Checks if panel is correctly shown to user
            panel = self.selenium.find_element(By.ID, f"{file_title}_panel_id")
            panels_style = panel.get_attribute("style")
            panels_title = panel.find_element(By.CLASS_NAME, "label_field").text
            self.assertEqual(panels_style, "display: block;")
            self.assertEqual(file_title, panels_title)
            
            time.sleep(1)
        
        print("[INFO] All buttons are clicked.")
        
        logger.info("TEST | Testing completed.")
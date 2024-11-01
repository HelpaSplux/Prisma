
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

import logging
import time

from .models import Notes, Users
from .test_utils import DBImage, create_records



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
    
    @staticmethod
    def get(test_object, url):
         # Adding sessionid in cookies
        session = test_object.client.session.session_key
        logger.info(f"Requesting {url}.")
        test_object.selenium.get(url)
        test_object.selenium.add_cookie({"name": "sessionid", "value": session,})
        
        # Refreshing the page to apply cookie changes 
        logger.info(f"Refreshing page.")
        test_object.selenium.refresh()
        time.sleep(1)
    
    
    
    
    
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
        
        
class TEST_CLOSE_FILES(SeleniumTest):
    def test(self):
        logger.info("Close files testing begins.")
        target_url = self.live_server_url + reverse("work-space:index")
        records = 10
        
        # Creates records in database
        dbi = DBImage()
        dbi.add_other_users(count=3, records=4)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        # Requesting target url
        self.get(self, target_url)
        
        
        
        # Clicks on all left buttons
        buttons = self.selenium.find_elements(By.CLASS_NAME, "file_button")
        logger.debug(f"Found {len(buttons)} buttons.")
        logger.info("Opening the left buttons.")
        for button in buttons:
            button.click()
              
        # Clicks tab 5
        tabs = self.selenium.find_elements(By.CLASS_NAME, "tab_button")
        tabs[5].click()

        
        # Closing files and making checks
        predictions = list(range(records)) # [0 1 2 3 4 5 6 7 8 9]
        predictions = predictions[::-1][5:] + predictions[6:] # [4 3 2 1 0 6 7 8 9 None]
        predictions.append(None)
        
        for prediction in predictions:
            
            # Finds components of current file
            closed_file = dict(
                left_button= self.selenium.find_element(By.CLASS_NAME, "file_button_active"),
                top_button = self.selenium.find_element(By.CLASS_NAME, "tab_button_active"),
                panel = self.selenium.find_element(By.XPATH, "/html/body/div[2]/div[@style='display: block;']"),
            )

            # Close current file
            close_button = closed_file["panel"].find_element(By.CLASS_NAME, "close_file_button")
            close_button.click()
            
            
            # Break the loop on the last iteration 
            if prediction == None:
                break
            
            
            # Finds components of current file
            opened_file = dict(
                left_button = self.selenium.find_element(By.CLASS_NAME, "file_button_active"),
                top_button = self.selenium.find_element(By.CLASS_NAME, "tab_button_active"),
                panel = self.selenium.find_element(By.XPATH, "/html/body/div[2]/div[@style='display: block;']/form/div[1]/textarea"),
            )


            # Checks if predicted file is opened
            self.assertIn(str(prediction), opened_file["left_button"].text)
            self.assertIn(str(prediction), opened_file["top_button"].text)
            self.assertIn(str(prediction), opened_file["panel"].text)
            
            # Checks if closed file components are changed
            self.assertEqual(closed_file["left_button"].get_attribute("class"), "file_button")
            self.assertEqual(closed_file["top_button"].get_attribute("class"), "tab_button")
            self.assertEqual(closed_file["top_button"].get_attribute("style"), "display: none;")
            self.assertEqual(closed_file["panel"].get_attribute("style"), "display: none;")



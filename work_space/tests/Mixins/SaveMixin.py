from selenium.webdriver.remote.webelement import WebElement

import time



class SaveMixin():
    
    def change_field(self, field: str, value: str):
        """
        Change field value.
        
        Valid field names:
            - title
            - content
        """
        
        file: dict = self.get_current_file()
        
        if field == "title": 
            field: WebElement = file["title_field"]
            
        elif field == "content": 
            field: WebElement = file["content_field"]
        
        else: raise ValueError("Invalid field name.")
        
        field.clear()
        field.send_keys(value)
        return


    def save_file(self): 
        file: dict = self.get_current_file()
        buttons: dict = {
            "save": file["save_button"],
            "menu": file["dropdown_menu"]
        }
        
        if not buttons["save"]: raise ValueError("Fail to click save button.")
        
        buttons["menu"].click()
        time.sleep(1)
        buttons["save"].click()
        return
        
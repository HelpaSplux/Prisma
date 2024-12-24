from selenium.webdriver.remote.webelement import WebElement

import time



class SaveMixin():
    
    def change_content(self): pass
    
    
    def change_title(self, new_title): 
        file: dict = self.get_current_file()
        field: WebElement = file["title_field"]
        
        field.clear()
        field.send_keys(new_title)
        return


    def save_file(self): 
        file: dict = self.get_current_file()
        buttons: dict = {
            "save": file["save_button"],
            "menu": file["dropdown_menu"]
        }
        
        if not buttons["save"]: raise ValueError("Fail to click save button.")
        
        buttons["menu"].click()
        time.sleep(0.7)
        buttons["save"].click()
        return
        
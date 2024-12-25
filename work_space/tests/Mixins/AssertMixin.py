from selenium.webdriver.remote.webelement import WebElement


class AssertMixin:
    
    def assert_everything_changed(self, new_title: str, new_content: str): 
        self.assert_title_changed(new_title)
        self.assert_content_changed(new_content)
        return
    
    
    def assert_nothing_changed(self): pass
    
    
    def assert_content_changed(self, new_content): 
        file: dict = self.get_current_file()
        field: WebElement = file["content_field"]
        field_text = field.get_attribute("value")
    
        self.assertEqual(field_text, new_content)    
        return
    
    
    def assert_title_changed(self, new_title: str): 
        file: dict = self.get_current_file()
        field: WebElement = file["title_field"]
        left_button: WebElement = file["left_button"]
        top_button: WebElement = file["top_button"]
        
        title: dict ={
            "panel": field.get_attribute("value"),
            "left_button": left_button.text,
            "top_button": top_button.text,
        }
        
        # Validate changes
        self.assertEqual(title["panel"], new_title)
        self.assertEqual(title["left_button"], new_title)
        self.assertEqual(title["top_button"], new_title)
        
        # Validate uniqueness 
        panels = self.get_panels()
        self.assert_unique_title(panels["left"], new_title)
        self.assert_unique_title(panels["top"], new_title)
        
        return
    
    def assert_unique_title(self, panel, title):
        title_count = panel.text.count(title)
        self.assertEqual(title_count, 1)
        return

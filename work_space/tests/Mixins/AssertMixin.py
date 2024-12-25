from selenium.webdriver.remote.webelement import WebElement


class AssertMixin:
    def assert_with_refresh(func):
        def inner(self: object, new_content: str | int):
            new_content = str(new_content)
            func(self, new_content)
            
            # Refresh
            self.selenium.refresh()
            self.open_file(self.first_file)
            func(self, new_content)
            
            # Check if changes are unique
            self.open_file(self.next_file)
            func(self, self.next_file)
            return
        return inner
    

    @assert_with_refresh
    def assert_content_changed(self, new_content: str | int): 
        file: dict = self.get_current_file()
        field: WebElement = file["content_field"]
        field_text = field.get_attribute("value")
    
        self.assertEqual(field_text, new_content)    
        return
    
    
    @assert_with_refresh
    def assert_title_changed(self, new_title: str | int): 
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

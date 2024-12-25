import logging

from .test_utils import DBImage, SeleniumTest



logger = logging.getLogger(__name__)
    
    
    
class TEST_CREATE_FILES(SeleniumTest):
    def test_create_files(self):
        logger.info("Testing begins.")
        self.go_to_the_site()
        
        # Create and validate files
        logger.info("First validation.")
        files = 3
        for file_name in range(files):
            self.create_file(file_name)
            self.assertCreated(file_name)
        
        # Validate total count of files
        logger.info("Second validation.")
        total_created_files = len(self._find_left_buttons())
        self.assertEqual(total_created_files, files)


class TEST_OPEN_FILES(SeleniumTest):
    def test_open_files(self):
        logger.info("Testing begins.")

        # Create records in database
        records = 5
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        self.go_to_the_site()
        
        # Open and validate files
        predictions = list(range(records))
        for prediction in predictions:
            self.open_file(prediction)
            
            opened_file = self.get_current_file()
            
            self.assertPrediction(prediction, opened_file)
            self.assertOpenedTab(opened_file)

        
class TEST_CLOSE_FILES(SeleniumTest):
    def test_close_files(self):
        logger.info("Testing begins.")
        # Creates records in database
        records = 7
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        
        self.go_to_the_site()
        
        self.open_files()
        
        middlepoint = int(records/2)
        predictions = list(range(records))
        predictions = predictions[::-1][middlepoint+1:] + predictions[middlepoint+1:]
        predictions.append(None)
        
        self.open_tab(middlepoint)
        
        # Close and validate files
        for prediction in predictions:
            closed_file = self.get_current_file()
            self.close_file(closed_file)
            self.assertClosed(closed_file)
            
            # Break the loop on the last iteration 
            if prediction == None: break
            
            opened_file = self.get_current_file()
            self.assertPrediction(prediction, opened_file)


class TEST_DELETE_FILES(SeleniumTest):
    def test_delete_files(self):
        records = 7
        
        logger.info("Testing begins.")
        
        # Creates records in database
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        
        self.go_to_the_site()
        self.open_files()
        
        middlepoint = int(records/2)
        predictions = list(range(records))
        predictions = predictions[::-1][middlepoint+1:] + predictions[middlepoint+1:]
        predictions.append(None)
        
        logger.debug(f"Variable predictions contains: {predictions}")
        
        self.open_tab(middlepoint)
        
        # Delete and validate files
        logger.info("Data validation")
        for prediction in predictions:
            deleted_file = self.get_current_file()
            self.delete_file(deleted_file)
            
            # Break the loop on the last iteration 
            if prediction == None: break
            
            opened_file = self.get_current_file()

            self.assertPrediction(prediction, opened_file)
            self.assertDeleted(deleted_file)


class TEST_SAVING_FILE(SeleniumTest):
    new_title = "New_title"
    new_content = "New_content"
    next_file = "1"
    
    
    def default_behavior(self):
        records = 3
        
        logger.info("Testing begins.")
        
        # Creates records in database
        dbi = DBImage()
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        self.go_to_the_site()
        self.open_file(0)   
        return
    
    
    
    def test_title_changed(self):
        self.default_behavior()
        
        self.change_field(field="title", value=self.new_title)
        
        self.save_file()
        
        # Validation
        self.assert_title_changed(self.new_title)
        self.selenium.refresh()
        self.open_file(0)
        self.assert_title_changed(self.new_title)
        return
    
    
    
    def test_content_changed(self):
        self.default_behavior()
        
        self.change_field(field="content", value=self.new_content)

        self.save_file()
    
    
        # Validation
        self.assert_content_changed(self.new_content)
        self.selenium.refresh()
        self.open_file(0)
        self.assert_content_changed(self.new_content)
        
        # Check if nothing else is changed
        self.open_file(self.next_file)
        self.assert_content_changed(self.next_file)
        return
        
        
    
    def test_everything_changed(self):
        self.default_behavior()
        
        self.change_field(field="title", value=self.new_title)
        self.change_field(field="content", value=self.new_content)
        
        self.save_file()
        
        self.assert_everything_changed(self.new_title, self.new_content)
        self.selenium.refresh()
        self.open_file(0)
        self.assert_everything_changed(self.new_title, self.new_content)
        
        
        self.open_file(self.next_file)
        self.assert_everything_changed(self.next_file, self.next_file)
        return
    
    
    
    # def test_nothing_changed(self):
    #     self.default_behavior()
        
    #     self.save_file()
        
    #     self.asser_nothing_changed()
    #     return
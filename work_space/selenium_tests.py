import logging

from .test_utils import DBImage, SeleniumTest



logger = logging.getLogger(__name__)
    
    
    
class TEST_CREATE_FILES(SeleniumTest):
    def test_create_files(self):
        logger.info("Testing begins.")
        self.go_to_the_site()
        
        # Create and validate files
        logger.info("First validation.")
        for file_name in range(10):
            self.create_file(file_name)
            self.assertCreated(file_name)
        
        # Validate total count of files
        logger.info("Second validation.")
        total_created_files = len(self._find_left_buttons())
        self.assertEqual(total_created_files, 10)


class TEST_OPEN_FILES(SeleniumTest):
    def test_open_files(self):
        logger.info("Testing begins.")

        # Create records in database
        records = 10
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        self.go_to_the_site()
        
        # Open and validate files
        logger.info("Data validation.")
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
        records = 10
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        
        self.go_to_the_site()
        
        self.open_files()
        self.open_tab(5)
        
        predictions = list(range(records))
        predictions = predictions[::-1][5:] + predictions[6:]
        predictions.append(None)
        
        # Close and validate files
        logger.info("Data validation.")
        for prediction in predictions:
            closed_file = self.get_current_file()
            self.close_file(closed_file)
            
            # Break the loop on the last iteration 
            if prediction == None: break
            
            opened_file = self.get_current_file()

            self.assertPrediction(prediction, opened_file)
            self.assertHidden(closed_file)


class TEST_DELETE_FILES(SeleniumTest):
    def test_delete_files(self):
        logger.info("Testing begins.")
        
        # Creates records in database
        records = 10
        dbi = DBImage()
        dbi.add_other_users(count=10, records=10)
        dbi.add_tested_user(test_object=self, records=records)
        dbi.create_records()
        
        
        self.go_to_the_site()
        
        self.open_files()
        self.open_tab(5)
        
        predictions = list(range(records))
        predictions = predictions[::-1][5:] + predictions[6:]
        predictions.append(None)
        
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

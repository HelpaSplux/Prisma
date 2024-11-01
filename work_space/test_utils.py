from psycopg2.errors import UniqueViolation

import logging

from .models import Notes, Users



logger = logging.getLogger(__name__)


def create_records(user: object = None, note: object = None, only_arguments: bool = False):
        '''
        Creates random records in tables 'users' & 'notes'.
        
        Can add additional records if it passes within keyword argumants
        
        If `only_arguments = True` creates only arguments you pass in.
        '''
        
        
        random_users = [
            Users(user="8e208yajayddm5mn5raof6feahyggb4w"),
            Users(user="7e608yzjayddm5mn5raof6feahyggb4w"),
       ]
        random_notes = [
            Notes(label="Parot", content="Just a tiny parot", user_id="8e208yajayddm5mn5raof6feahyggb4w"),
            Notes(label="Smoll", content="So smoll", user_id="8e208yajayddm5mn5raof6feahyggb4w"),
            Notes(label="The spirit city", content="There are only spirits", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
            Notes(label="Power bank", content="Power", user_id="7e608yzjayddm5mn5raof6feahyggb4w"),
       ]

        # Adds specified arguments to random records
        if only_arguments:
            logger.info("Clearing all tables...")
            random_users.clear()
            random_notes.clear()
            logger.info("Complete.")
        
        if user:
            logger.info(f"Adding to random_users list - {user}...")
            random_users.append(user)
            logger.info("Complete.")
            
        if note:
            logger.info(f"Adding to random_notes list - {note}...")
            random_notes.append(note)
            logger.info("Complete.")
        
        logger.debug(f"Variable random_users contains {len(random_users)} records - {random_users}")
        logger.debug(f"Variable random_notes contains {len(random_notes)} records - {random_notes}")
        
        # Create records in table 'users'
        try:
            logger.info("USER | Attempting to create records in table 'users'...")
            Users.objects.bulk_create(random_users)
            logger.info("USER | Complete.")
        except UniqueViolation:
            logger.info("USER | Failed to cretae a user.")
            logger.warning("USER | This user already exists")
            
        # Create records in table 'notes'
        try:
            logger.info("Attempting to create records in table 'notes'...")
            Notes.objects.bulk_create(random_notes)
            logger.info("Complete.")
        except UniqueViolation:
            logger.info("NOTE | Failed to cretae a note.")
            logger.warning("NOTE | This note already exists")
            
class DBImage():
    '''
    Creates database image and allows you to create DB records based on this image.
    '''
    
    def __init__(self):
        self.users = []
        self.notes = []
        return
    
    @staticmethod
    def __create_note_models(self, records: int, user_id: str | int = None) -> None:
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
                    __class__.__create_note_models(self, records, user_number)
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
            __class__.__create_note_models(self, records, session)
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

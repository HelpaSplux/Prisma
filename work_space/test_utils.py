import logging

from .models import Notes, Users



logger = logging.getLogger(__name__)


def create_records(user: object = None, note: object = None, empty_tables: bool = False):
        '''
        Creates random records in tables 'users' & 'notes'.
        
        Can add additional records if it passes within keyword argumants
        
        If `all_tables_empty = True` creates only arguments you pass in.
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
        if empty_tables:
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
        logger.info("Attempting to create records in table 'users'...")
        Users.objects.bulk_create(random_users)
        logger.info("Complete.")
        
        
        # Create records in table 'notes'
        logger.info("Attempting to create records in table 'notes'...")
        Notes.objects.bulk_create(random_notes)
        logger.info("Complete.")
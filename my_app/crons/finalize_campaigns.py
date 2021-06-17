import logging

from sqlalchemy.orm import sessionmaker


def finalize_campaign(session_factory: sessionmaker):
    logging.info("Finishing campaigns")
    """ 
    Code example for database operations
    
    with session_factory() as session:
        printer_user_model = UserModel(first_name='Cronjob',
                                       last_name='Cronjob',
                                       user_name='Cronjob',
                                       date_of_birth=datetime.now(),
                                       email='Cronjob@gmail.com')
        session.add(printer_user_model)
        session.commit()
    """

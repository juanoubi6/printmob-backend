import logging
import time
from typing import List

from my_app.api.utils.email import Email


class EmailRepository:

    def send_individual_email(self, email: Email):
        try:
            time.sleep(3)
            print("Email sent to {}".format(email.to))
        except Exception as exc:
            logging.error("Email could not be sent: {}".format(str(exc)))

    def send_many_emails(self, email_list: List[Email]):
        try:
            time.sleep(10)
            print("Emails sent. Amount: {}".format(len(email_list)))
        except Exception as exc:
            logging.error("Error sending emails: {}".format(str(exc)))

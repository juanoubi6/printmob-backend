import logging
from typing import List

from my_app.api.utils.email import Email


class EmailRepository:
    def __init__(self, ses_client, sender_email: str):
        self.ses_client = ses_client
        self.sender_email = sender_email

    def send_individual_email(self, email: Email):
        try:
            self.ses_client.send_email(
                Source=self.sender_email,
                Destination={
                    'ToAddresses': [email.to],
                    'CcAddresses': [],
                    'BccAddresses': []
                },
                Message={
                    'Subject': {
                        'Data': email.subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': email.body,
                        }
                    }
                }
            )
            print("Email sent to {}".format(email.to))
        except Exception as exc:
            logging.error("Email could not be sent: {}".format(str(exc)))

    def send_many_emails_of_the_same_type(self, email_list: List[Email]):
        if len(email_list) == 0:
            return

        try:
            self.ses_client.send_email(
                Source=self.sender_email,
                Destination={
                    'ToAddresses': [self.sender_email],
                    'CcAddresses': [],
                    'BccAddresses': [email.to for email in email_list]
                },
                Message={
                    'Subject': {
                        'Data': email_list[0].subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': email_list[0].body,
                        }
                    }
                }
            )
            print("Emails sent. Amount: {}".format(len(email_list)))
        except Exception as exc:
            logging.error("Error sending emails: {}".format(str(exc)))

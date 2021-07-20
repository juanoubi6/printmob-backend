import unittest
from unittest.mock import MagicMock

from my_app.api.repositories import EmailRepository
from my_app.api.utils.email import Email

sender_email = "sender_email@email.com"


class TestEmailRepository(unittest.TestCase):

    def setUp(self):
        self.test_ses_client = MagicMock()
        self.email_repository = EmailRepository(self.test_ses_client, sender_email)

    def test_send_individual_email_does_not_throw_error_on_failure(self):
        self.test_ses_client.send_email.side_effect = Exception("Some SES error")

        self.email_repository.send_individual_email(Email(to="to", subject="subject", body="body"))

        self.test_ses_client.send_email.assert_called_once()

    def test_send_many_emails_of_the_same_type_does_not_throw_error_on_failure(self):
        self.test_ses_client.send_email.side_effect = Exception("Some SES error")

        self.email_repository.send_many_emails_of_the_same_type([Email(to="to", subject="subject", body="body")])

        self.test_ses_client.send_email.assert_called_once()

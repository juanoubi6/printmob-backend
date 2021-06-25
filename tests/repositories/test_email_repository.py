import unittest
from unittest.mock import MagicMock, patch

from my_app.api.repositories import EmailRepository
from my_app.api.utils.email import Email

test_ses_client = MagicMock()
sender_email = "sender_email@email.com"
email_repository = EmailRepository(test_ses_client, sender_email)


class TestEmailRepository(unittest.TestCase):

    def setUp(self):
        test_ses_client.reset_mock()

    @patch.object(test_ses_client, 'send_email')
    def test_send_individual_email_does_not_throw_error_on_failure(self, send_email_mock):
        send_email_mock.side_effect = Exception("Some SES error")

        email_repository.send_individual_email(Email(to="to", subject="subject", body="body"))

        send_email_mock.assert_called_once()

    @patch.object(test_ses_client, 'send_email')
    def test_send_many_emails_of_the_same_type_does_not_throw_error_on_failure(self, send_email_mock):
        send_email_mock.side_effect = Exception("Some SES error")

        email_repository.send_many_emails_of_the_same_type([Email(to="to", subject="subject", body="body")])

        send_email_mock.assert_called_once()

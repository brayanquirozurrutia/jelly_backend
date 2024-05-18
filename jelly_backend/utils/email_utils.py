from __future__ import print_function
import os
import sib_api_v3_sdk

from dotenv import load_dotenv
from jelly_backend.docs.sendinblue import lists, email_templates
from pprint import pprint
from sib_api_v3_sdk.rest import ApiException

load_dotenv()


class SendinblueClient:
    """
    This class is used to interact with the Sendinblue API.
    It is used to create contacts, add contacts to a list, and send emails.
    """

    def __init__(self):
        """
        Initializes the Sendinblue client.
        """
        self.configuration = sib_api_v3_sdk.Configuration()
        api_key = os.getenv('SENDINBLUE_API_KEY')
        if not api_key:
            raise ValueError("SENDINBLUE_API_KEY is not set in the environment variables.")
        self.configuration.api_key['api-key'] = api_key
        self.contacts_api = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        self.emails_api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))

    def create_contact(self, email: str, first_name: str, last_name: str) -> None:
        """
        Creates a new contact in Sendinblue.
        :param email: The email of the contact.
        :param first_name: The first name of the contact.
        :param last_name: The last name of the contact.
        :return: None
        """
        contact = sib_api_v3_sdk.CreateContact(
            email=email,
            attributes={
                'NOMBRE': first_name,
                'APELLIDOS': last_name
            }
        )
        try:
            api_response = self.contacts_api.create_contact(contact)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)

    def add_contact_to_list(self, email_to_add: str) -> None:
        """
        Adds a contact to a list in Sendinblue.
        :param email_to_add: The email of the contact to add.
        :return: None
        """
        list_id = lists['Accounts Created']
        contact_emails = sib_api_v3_sdk.AddContactToList(emails=[email_to_add])
        try:
            api_response = self.contacts_api.add_contact_to_list(list_id, contact_emails)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->add_contact_to_list: %s\n" % e)

    def send_welcome_email(self, email: str, first_name: str, last_name: str) -> None:
        """
        Sends a welcome email to a new user.
        :param email: The email of the user.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :return: None
        """
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Welcome Email'],
            params={
                'NOMBRE': first_name,
                'APELLIDOS': last_name
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

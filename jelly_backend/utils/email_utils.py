from __future__ import print_function
import os
import sib_api_v3_sdk

from dotenv import load_dotenv
from pprint import pprint
from jelly_backend.docs.sendinblue import lists, email_templates
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

    def create_contact(self, email: str, full_name: str, first_name: str, last_name: str) -> None:
        """
        Creates a new contact in Sendinblue.
        :param email: The email of the contact.
        :param full_name: The full name of the contact.
        :param first_name: The first name of the contact.
        :param last_name: The last name of the contact.
        :return: None
        """
        contact = sib_api_v3_sdk.CreateContact(
            email=email,
            attributes={
                'FULL_NAME': full_name,
                'NOMBRE': first_name,
                'APELLIDOS': last_name
            }
        )
        try:
            api_response = self.contacts_api.create_contact(contact)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)

    def update_contact(self, email: str, attributes: dict) -> None:
        """
        Updates a contact in Sendinblue.
        :param email: The identifier of the contact. (email)
        :param attributes: The attributes to update.
        :return:
        """
        update_contact = sib_api_v3_sdk.UpdateContact(
            attributes=attributes
        )
        try:
            api_response = self.contacts_api.update_contact(email, update_contact)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->update_contact: %s\n" % e)

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

    def activate_account_email(self, email: str, full_name: str, activation_code: str) -> None:
        """
        Sends an activation email to a new user.
        :param email: The email of the user.
        :param full_name: The full name of the user.
        :param activation_code: The activation code.
        :return: None
        """
        # We update the contact with the activation code
        self.update_contact(
            email=email,
            attributes={
                'ACTIVATE_ACCOUNT_CODE': activation_code
            }
        )
        # We send the email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Account Activation Email'],
            params={
                'FULL_NAME': full_name,
                'ACTIVATE_ACCOUNT_CODE': activation_code
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

    def send_welcome_email(self, email: str, full_name: str) -> None:
        """
        Sends a welcome email to a new user.
        :param email: The email of the user.
        :param full_name: The full name of the user.
        :return: None
        """
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Welcome Email'],
            params={
                'FULL_NAME': full_name
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

    def send_account_activated_email(self, email: str, full_name: str) -> None:
        """
        Sends an account activated email to a user.
        :param email: The email of the user.
        :param full_name: The full name of the user.
        :return: None
        """
        # We update the contact with the activation code
        self.update_contact(
            email=email,
            attributes={
                'ACTIVATE_ACCOUNT_CODE': 0
            }
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Account activated Email'],
            params={
                'FULL_NAME': full_name
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

    def send_forgot_password_email(self, email: str, full_name: str, reset_code: str) -> None:
        """
        Sends a forgot password email to a user.
        :param email: The email of the user.
        :param full_name: The full name of the user.
        :param reset_code: The reset code.
        :return: None
        """
        # We update the contact with the reset code
        self.update_contact(
            email=email,
            attributes={
                'RESET_PASSWORD_CODE': reset_code
            }
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Forgot Password Email'],
            params={
                'FULL_NAME': full_name,
                'RESET_PASSWORD_CODE': reset_code
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

    def send_password_changed_email(self, email: str, full_name: str) -> None:
        """
        Sends a password changed email to a user.
        :param email: The email of the user.
        :param full_name: The full name of the user.
        :return: None
        """
        # We update the contact
        self.update_contact(
            email=email,
            attributes={
                'RESET_PASSWORD_CODE': 0
            }
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            template_id=email_templates['Password Changed Email'],
            params={
                'FULL_NAME': full_name
            }
        )
        try:
            api_response = self.emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

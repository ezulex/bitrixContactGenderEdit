import requests
import app_logger
import os
from dotenv import load_dotenv

logger = app_logger.get_logger(__name__)
load_dotenv()

domain = os.environ.get("BITRIX_DOMAIN")
user_id = os.environ.get("BITRIX_USER_ID")
auth_key = os.environ.get("BITRIX_AUTH_KEY")
area_id = os.environ.get("BITRIX_AREA_ID")
area_man = os.environ.get("BITRIX_AREA_MAN")
area_woman = os.environ.get("BITRIX_AREA_WOMAN")


def get_contact_name_by_id(contact_id):
    """
            This function get contact name by id from Bitrix
            contact_id: integer, contact id from bitrix
    """
    webhook_url = f'https://{domain}.bitrix24.ru/rest/{user_id}/{auth_key}/crm.contact.get.json'
    data = {
        'id': contact_id
    }

    try:
        response_webhook = requests.post(webhook_url, json=data)
        response_webhook.raise_for_status()
        response_json = response_webhook.json()
        response = response_json["result"]["NAME"]
        logger.info(f'Webhook get_contact_name_by_id for name: {response}')
        return response
    except requests.exceptions.RequestException as error:
        logger.error(f"Error with webhook get_contact_name_by_id: {error}")


def edit_contact_sex_by_id(contact_id, contact_sex):
    """
        This function change sex of an existing contact
        contact_id: integer, contact id from Bitrix
        contact_sex: string, contact sex can be 0 - female or 1 - male
    """
    webhook_url = f'https://{domain}.bitrix24.ru/rest/{user_id}/{auth_key}/crm.contact.update.json'

    if contact_sex == 1:
        contact_sex_id = area_man
    elif contact_sex == 0:
        contact_sex_id = area_woman
    else:
        logger.error(f"Wrong params for edit_contact_sex_by_id")
        return False
    data = {
        'id': contact_id,
        "fields": {
            area_id: contact_sex_id
        }
    }

    try:
        response_webhook = requests.post(webhook_url, json=data)
        response_webhook.raise_for_status()
        response_json = response_webhook.json()
        response = response_json["result"]
        logger.info(f'webhook edit_contact_sex_by_id status: {response_webhook.status_code}')
        return response
    except requests.exceptions.RequestException as error:
        logger.error(f"Error with webhook edit_contact_sex_by_id: {error}")

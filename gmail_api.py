import os
import pickle
import logging
import re
# Gmail API utils
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64decode, urlsafe_b64encode
from mimetypes import guess_type as guess_mime_type

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from decouple import config
# from logger import get_logger

# LOGGER = get_logger()
OUR_EMAIL = config("YOUR_GMAIL")
# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']

def gmail_authenticate():
    creds = None
    if os.path.exists(".secrets/token.pickle"):
        with open(".secrets/token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('.secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open(".secrets/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def parse_unsub_header(message_unsub):
    if not message_unsub:
        return None
    
    if "mailto" not in message_unsub:
        return None
    
    regex_for_mailto = r"\<mailto:([^\?]*)\>"
    match = re.search(regex_for_mailto, message_unsub)
    if match:
        return match.group(1).split(">")[0]
    else:
        return None

def parse_message(message):
    message_id = message["id"]
    list_unsub = None
    message_from = None
    message_headers = message["payload"]["headers"]

    for header in message_headers:
        if header["name"] == "List-Unsubscribe":
            list_unsub = header["value"]
        if header["name"] == "From":
            message_from = header["value"]

    return {
        "message_id": message_id,
        "message_unsub": list_unsub,
        "processed_message_unsub": parse_unsub_header(list_unsub),
        "message_from": message_from,
    }


def search_messages_for_unsubscribe(service, msg_content = [], page_token=None, iter=1, limit_iter=20):
    
    if iter == limit_iter:
        return msg_content
    
    # LOGGER.info(f'Searching for messages to unsubscribe, iteration {iter}')
    query = {
        "q": 'in:all "unsubscribe" | "desinscrever"',
        "userId": "me",
    }

    if page_token:
        query["pageToken"] = page_token

    result = service.users().messages().list(**query).execute()

    for message in tqdm(result["messages"]):
        msg = parse_message(service.users().messages().get(
            userId='me',
            id=message['id'],
            format='full'
        ).execute())
        if msg['processed_message_unsub']:
            msg_content.append(msg)
        

    return search_messages_for_unsubscribe(
        service,
        msg_content=msg_content,
        page_token=result['nextPageToken'],
        iter=iter+1,
        limit_iter=limit_iter
    )

def create_message_without_attachment(destination):
    message = MIMEText("")
    message['to'] = destination
    message['from'] = OUR_EMAIL
    message['subject'] = "Unsubscribe"
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination):
    return service.users().messages().send(
      userId="me",
      body=create_message_without_attachment(destination)
    ).execute()
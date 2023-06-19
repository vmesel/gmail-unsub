import pandas as pd

from gmail_api import *
service = gmail_authenticate()
# from pprint import pprint as print
from logger import get_logger

LOGGER = get_logger()

print(" ==== GMAIL UNSUB STARTED ==== ")
print("Getting unsubscription emails from previous messages")

message_items = search_messages_for_unsubscribe(service, limit_iter=20)

df = pd.DataFrame(message_items)
df = df[df["processed_message_unsub"].notnull()]
df = df.drop_duplicates(subset=["processed_message_unsub"])
df = df[["message_from", "processed_message_unsub"]]
df.to_csv("emails_to_unsub.csv", index=False)

print("Finished generating emails to unsubscribe list, edit it and run\n\n`python unsubscribe.py`\n\nto unsubscribe from these emails")
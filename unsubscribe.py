import pandas as pd

from gmail_api import *
service = gmail_authenticate()
# from pprint import pprint as print

df = pd.read_csv("emails_to_unsub.csv")
df = df[df["processed_message_unsub"].notnull()]

for index, row in df.iterrows():
    row = row.to_dict()
    print("Unsubscribing from: {}".format(row["processed_message_unsub"]))
    # send_message(service, row["processed_message_unsub"])
    print("Unsubscribed from: {}".format(row["message_from"]))

print(" ==== GMAIL UNSUB FINISHED ==== ")

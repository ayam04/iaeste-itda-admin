import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import re
from streamlit_gsheets import GSheetsConnection

def init():
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

def add_to_firebase(email_id,name):
    db = firestore.client()
    db_collection = db.collection("user")
    
    query = db_collection.order_by('_id', direction=firestore.Query.DESCENDING).limit(2)
    result = query.get()
    last_doc_id = result[1].id
    new_doc_id = next_id(last_doc_id)

    doc_ref = db_collection.document(new_doc_id)
    
    data = {
        "_id": f"{new_doc_id}",
        "email_id" : f"{email_id}",
        "name": f"{name}"
    }

    doc_ref.set(data)

def next_id(code):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    part = list(code)

    a = part[-1]
    b = part[-2]
    c = part[-3]
    d = part[-4]
    e = part[-5]

    idx = alphabet.index(c)

    if a == "9":
        if b == "9":
            if idx == 25:
                if d == "9":
                    a = 1
                    b = 0
                    c = alphabet[0]
                    d = 0
                    e = int(e) + 1
                else:    
                    d = int(d) + 1
                    a = 1
                    b = 0
            else:
                c = alphabet[idx + 1]
                a = 1
                b = 0
        else:
            b = int(part[-2]) + 1
            a = 0
    else:
        a = int(part[-1]) + 1

    final = f"{e}{d}{c}{b}{a}"
    return final

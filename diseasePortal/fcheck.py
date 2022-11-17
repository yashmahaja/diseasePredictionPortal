import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('diseasefire.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

prediction = 85
docs = db.collection('data').where("pred1", "==", prediction).limit(1).get()
for doc in docs:
    a = doc.to_dict()
    print(a)
# patients = [patient.to_dict() for patient in patients]
# for patient_obj in patients:
#     print(patient_obj.albumin)
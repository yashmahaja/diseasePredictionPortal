import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('D:/Propy/Django/diseasePortal/diseasePortal/diseasefire.json')

firebase_admin.initialize_app(cred, 
{
'databaseURL': 'https://diseaseportal-default-rtdb.firebaseio.com/'
})

db = firestore.client()
doc_ref = db.collection(u'data')# Import data
df = pd.read_csv('D:/Propy/Django/diseasePortal/preprcessed.csv')
tmp = df.to_dict(orient='records')
list(map(lambda x: doc_ref.add(x), tmp))
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('diseasefire.json')

firebase_admin.initialize_app(cred, 
{
'databaseURL': 'https://diseaseportal-default-rtdb.firebaseio.com/'
})

db = firestore.client()
doc_ref = db.collection(u'data')# Import data
df = pd.read_csv('ab.csv')
tmp = df.to_dict(orient='records')
list(map(lambda x: doc_ref.add(x), tmp))
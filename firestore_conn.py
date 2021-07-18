import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Connect to Firestore with service account
print(f'>>> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Started connecting to Firestore database...')
firestore_key = r'your_service_account_file.json'  # Prod
cred = credentials.Certificate(firestore_key)
app = firebase_admin.initialize_app(cred)
db = firestore.client(app=app)
print(f'<<< {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Firestore database connected \n---')

try:
    # Firestore operations, such as
    doc_ref = db.collection('coll_id').document('doc_id')
except Exception as e_read_write:
    print(f'??? {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Exception in doing...:', e_read_write)
else:
    print(f'<<< {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Finished doing...\n---')
from google.cloud import firestore
from os.path import abspath


def init_db():
    db = False
    db = firestore.Client.from_service_account_json(abspath('google-config.json'))
    # db = firestore.Client(project="infinity-clinic-359114")
    print(f"DB initialized {db.project}")
    return db

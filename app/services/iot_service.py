from ..models.base import BaseModel
from google.cloud.firestore_v1.base_query import FieldFilter

class IOTService:
    collection_name = 'iot'
    baseModel = BaseModel()

    def create(self, db, item):
            data = self.baseModel.withIdAndTimeStamp(item)
            iotRef = db.collection(self.collection_name)
            result = iotRef.document(data['id']).set(data)
            print(result)
            return data
    
    def readByPatientId(self, db, patient_id):
            docs = db.collection(self.collection_name).where(filter=FieldFilter("patient_id", "==", patient_id)).stream()
            result = []
            for doc in docs:
                result.append(doc.to_dict())
            return result
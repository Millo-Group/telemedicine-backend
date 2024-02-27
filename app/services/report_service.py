from ..models.base import BaseModel
from google.cloud.firestore_v1.base_query import FieldFilter

class ReportService:
    collection_name = 'reports'
    baseModel = BaseModel()

    def create(self, db, item):
            item["file"] = str(item['file'])
            data = self.baseModel.withIdAndTimeStamp(item)
            iotRef = db.collection(self.collection_name)
            iotRef.document(data['id']).set(data)
            return data
    
    def readByPatientId(self, db, patient_id):
            docs = db.collection(self.collection_name).where(filter=FieldFilter("patient_id", "==", patient_id)).stream()
            result = []
            for doc in docs:
                result.append(doc.to_dict())
            return result
        
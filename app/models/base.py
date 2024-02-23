import uuid
import datetime

class BaseModel(object):

    def withIdAndTimeStamp(self, item):
        id = str(uuid.uuid4())
        timestamp = str(datetime.datetime.now().isoformat())
    
        item["id"] = id
        item['timestamp'] = timestamp
        return item
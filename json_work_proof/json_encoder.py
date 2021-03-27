import json
from datetime import datetime

class DefaultJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.timestamp()
        
        return json.JSONEncoder.default(self, obj)
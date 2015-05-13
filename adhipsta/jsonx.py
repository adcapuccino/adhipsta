import json
from asyncio_mongo._bson.objectid import ObjectId


class ObjectIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def dumps(obj):
    return json.dumps(obj, cls=ObjectIdEncoder)

def loads(*av, **kw):
    return json.loads(*av, **kw)

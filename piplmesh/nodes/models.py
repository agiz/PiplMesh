import mongoengine

class Node(mongoengine.Document):
    # TODO: better id field
    id = mongoengine.StringField(max_length=255, primary_key=True)
    address = mongoengine.StringField(max_length=255)
    location = mongoengine.GeoPointField()
    name = mongoengine.StringField(max_length=150)
    url = mongoengine.StringField(max_length=255)
    _outside_request = mongoengine.BooleanField(default=False)
    last_update = mongoengine.DateTimeField()

class OCVenue(mongoengine.Document):
    oc_node = mongoengine.StringField()
    oc_address = mongoengine.StringField(max_length=255)
    oc_distance = mongoengine.StringField(max_length=32)
    oc_location = mongoengine.GeoPointField()
    oc_name = mongoengine.StringField(max_length=255)
    oc_is_open = mongoengine.BooleanField()
    oc_timeleft = mongoengine.StringField(max_length=255)
    oc_open_hours = mongoengine.DictField()
    oc_extra = mongoengine.ListField()
    oc_last_update = mongoengine.DateTimeField()
    
class NodeModel(object):
    def __init__(self, id, name, location, latitude, longitude, url):
        self.id = id
        self.name = name
        self.address = location
        self.location = [latitude, longitude]
        self.url = url
        
        self._outside_request = False

    def is_outside_request(self):
        return self._outside_request

    def is_inside_request(self):
        return not self._outside_request
import json


class ConnectionModel:
    def __init__(self):
        self.device_name = None
        self.ip_address = None
        self.ipv6_local_address = None
        self.ipv6_global_address = None
        self.mac_address = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()

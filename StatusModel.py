import json


class StatusModel:
    def __init__(self):
        self.hostname = None
        self.model = None
        self.mac_address = None
        self.firmware = None
        self.dsl_version = None
        self.dsl_mode = None
        self.annex_type = None
        self.wan_information = [None] * 8
        self.lan = LanInfo()
        self.wlan = WLanInfo()
        self.interface_status = []
        self.current_time = None
        self.pppoe_uptime = None
        self.cpu_usage = None
        self.memory_usage = None
        self.dsl_down_bandwidth = None
        self.dsl_up_bandwidth = None
        self.system_uptime = None
        self.dsl_uptime = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()


class WanInfoPVC:
    def __init__(self):
        self.stack = None
        self.ip_address = None
        self.subnet_mask = None
        self.default_gateway = None
        self.primary_dns = None
        self.secondary_dns = None
        self.ipv6_global_address = None
        self.ipv6_prefix_length = None
        self.ipv6_gateway = None
        self.ipv6_primary_dns = None
        self.ipv6_secondary_dns = None
        self.ipv6_local_address = None
        self.mtu = None
        self.vpi_vci = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()


class LanInfo:
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.dhcp = None
        self.ipv6_address = None
        self.ipv6_local_address = None
        self.ipv6_prefix = None
        self.ipv6_valid_time = None
        self.ipv6_dhcp = None
        self.radvd_state = None
        self.ipv6_primary_dns = None
        self.ipv6_secondary_dns = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()


class WLanInfo:
    def __init__(self):
        self.status = None
        self.ssid = None
        self.channel = None
        self.security = None
        self.wps = None
        self.scheduling = None
        self.firewall = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()


class InterfaceStatus:
    def __init__(self):
        self.interface = None
        self.status = None
        self.rate = None

    def __str__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __repr__(self):
        return self.__str__()

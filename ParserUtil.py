import re

from bs4 import BeautifulSoup

from ConnectionModel import ConnectionModel
from StatusModel import StatusModel, WanInfoPVC, InterfaceStatus


def parse_connections(source):
    print(":: Parsing Main Page")
    # Fix broken html -.-
    source = source.replace('<td class="table_font">\n</ul></li>', '<td class="table_font">\n')
    soup = BeautifulSoup(source, 'html.parser')

    connections_info = []

    table_source = str(soup.find(id="MLG_Device_Name").parent.parent.parent)

    table_source = table_source
    table_soup = BeautifulSoup(table_source, 'html.parser')

    entries = list(table_soup.find_all("tr"))[1:]

    for entry in entries:
        entry = list(map(lambda x: x.text.strip(), entry.find_all("td")))
        connection = ConnectionModel()
        connection.device_name = entry[1]
        connection.ip_address = entry[2]
        connection.ipv6_local_address = entry[3]
        connection.ipv6_global_address = entry[4]
        connection.mac_address = entry[5]
        connections_info.append(connection)

    return connections_info


def _get_table_value(soup, find_id):
    v = soup.find(id=find_id).parent.next_sibling
    if v == '\n':
        v = v.next_sibling

    return v.text.strip()


# Because *some* fields are just a bit special -.-
def _get_table_value_string(soup, find_key):
    v = soup.find("td", string=re.compile(find_key)).next_sibling
    if v == '\n':
        v = v.next_sibling

    return v.string.strip()


def parse_status(source):
    print(":: Parsing Status page")
    soup = BeautifulSoup(source, 'html.parser')

    # Private util methods
    def _get(find_id):
        return _get_table_value(soup, find_id)

    def _find(find_str):
        return _get_table_value_string(soup, find_str)

    def _get_usage(find_id):
        return list(soup.find(id=find_id).parent.parent.find_all("td"))[-1].text.strip()

    status = StatusModel()

    #
    # Parse Device info
    #

    status.hostname = _get("HostName_ConnectionStatus")
    status.model = _get("ModelName_ConnectionStatus")
    status.mac_address = _get("MACAddressColon_ConnectionStatus")
    status.firmware = _get("MLG_FirmwareVersion_ConnectionStatus")
    status.dsl_version = _get("MLG_DSL_Version")
    status.dsl_mode = _get("MLG_DSL_Mode")
    status.annex_type = _get("MLG_Home_Annex_Type")

    status.wan_information[0] = WanInfoPVC()
    status.wan_information[0].stack = _get("MLG_v4v6DualStack_Broadband")
    status.wan_information[0].ip_address = _get("MLG_IP_Address2")
    status.wan_information[0].subnet_mask = _get("MLG_IP_Subnet_Mask")
    status.wan_information[0].default_gateway = _get("MLG_Default_Gateway")
    status.wan_information[0].primary_dns = _get("MLG_Primary_DNS")
    status.wan_information[0].secondary_dns = _get("MLG_Second_DNS")
    status.wan_information[0].ipv6_global_address = _get("MLG_IPv6_Glob_Addr")
    status.wan_information[0].ipv6_prefix_length = _get("MLG_Home_IPv6_Prefix_length")
    status.wan_information[0].ipv6_gateway = _get("MLG_Home_IPv6_DefGW")
    status.wan_information[0].ipv6_primary_dns = _get("MLG_IPv6_WAN_DNS1")
    status.wan_information[0].ipv6_secondary_dns = _get("MLG_IPv6_WAN_DNS2")
    status.wan_information[0].ipv6_local_address = _get("MLG_Home_IPv6_Addr")
    status.wan_information[0].mtu = _find("MTU")
    status.wan_information[0].vpi_vci = _find("VPI/VCI").replace("\n", "")

    # lan
    status.lan.ip_address = _get("MLG_IP_Address")
    status.lan.subnet_mask = _get("MLG_IP_Subnet_Mask2")
    status.lan.dhcp = _find("DHCP")
    status.lan.ipv6_address = _get("MLG_wan_IPv6_Addr")
    status.lan.ipv6_local_address = _get("MLG_IPv6_Linklocal_Address")
    status.lan.ipv6_prefix = _get("MLG_Home_IPv6_Prefix")
    status.lan.ipv6_valid_time = _get("ZYXEL_IPv6_Valid_Time")
    status.lan.ipv6_dhcp = _find("DHCPv6")
    status.lan.radvd_state = _get("ZYXEL_IPv6_Radvd_State")
    status.lan.ipv6_primary_dns = _get("MLG_IPv6_LAN_DNS1")
    status.lan.ipv6_secondary_dns = _get("MLG_IPv6_LAN_DNS2")

    # WLAN
    status.wlan.status = _get("MLG_Home_Status")
    status.wlan.ssid = _find("SSID")
    status.wlan.channel = _get("MLG_Channel_Wireless")
    status.wlan.security = _get("MLG_Home_Security_Mode")
    status.wlan.wps = _find("WPS")
    status.wlan.scheduling = _get("MLG_Scheduling")
    status.wlan.firewall = _get("MLG_Home_Firewall")


    #
    # Interface status
    #
    intrf_table = soup.find("span", id="MLG_Interface").parent.parent

    cur_row = intrf_table.next_sibling
    while cur_row:
        if cur_row == '\n':
            cur_row = cur_row.next_sibling
            continue

        row = cur_row.find_all("td")
        intf = InterfaceStatus()
        interface_name = row[0].text.strip()
        intf.interface = interface_name if interface_name else row[0].find("span").attrs['id'] # TODO: "translate"
        intf.status = row[1].text.strip()
        intf.rate = row[2].text.strip()

        status.interface_status.append(intf)
        cur_row = cur_row.next_sibling

    #
    # System status
    #
    status.current_time = _get("MLG_Current_Time_Date")
    status.pppoe_uptime = _get("MLG_PPPoE_UpTime").replace(':', ' ').replace('\n', '')
    status.cpu_usage = _get_usage("MLG_Home_CPU")
    status.memory_usage = _get_usage("MLG_Home_MemUsage")
    status.dsl_down_bandwidth = _get_usage("DSL_Down_Bandwidth_Usage_Text")
    status.dsl_up_bandwidth = _get_usage("DSL_Up_Bandwidth_Usage_Text")

    # because they are special -.-
    status.system_uptime = ""
    sys_uptime_element = soup.find(id="MLG_Home_SysUp").parent.next_sibling.children
    for element in sys_uptime_element:
        if isinstance(element, str):
            status.system_uptime += ' ' + element.replace('\n', '').replace(':', '').strip()
        else:
            status.system_uptime += element.attrs.get('id').replace('MLG_Status_SysUpTime_', ' ')


    status.dsl_uptime = ""
    dsl_uptime_element = soup.find(id="MLG_Home_DSL_UpTime").parent.next_sibling.next_sibling.children
    for element in dsl_uptime_element:
        if isinstance(element, str):
            status.dsl_uptime += ' ' + element.replace('\n', '').replace(':', '').strip()
        else:
            status.dsl_uptime += element.attrs.get('id').replace('MLG_Status_AdslUpTime_', ' ')

    return status
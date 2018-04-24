import base64
from time import sleep

import requests

BASE_URL = "http://192.168.1.1"

cookies = None
logged_in = False


def get_session():
    print(":: Creating Session")
    global cookies
    r = requests.get(BASE_URL, allow_redirects=False)

    cookies = r.cookies


def login(username, password):
    if cookies is None:
        get_session()

    print(":: Logging in...")
    query_str = base64.encodebytes(f"{username}:{password}".encode('utf-8')).decode('utf-8').strip()

    url = f"{BASE_URL}/cgi-bin/index.asp?{query_str}"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = f"LoginUser={username}\n"

    r = requests.post(url, data=data, headers=headers, cookies=cookies)

    if "jumpUrl" not in r.text or "passWarning" not in r.text:
        print("::  > Failed")
        exit(1)

    global logged_in
    logged_in = True
    print("::  > Success")


def get_connections_html():
    print(":: Fetching connections page")
    if not logged_in:
        raise ValueError("Must login")

    r = requests.get(f"{BASE_URL}/cgi-bin/pages/connectionStatus.cgi", cookies=cookies)

    return r.text


def get_status_html():
    print(":: Fetching Status page")
    if not logged_in:
        raise ValueError("Must login")

    r = requests.get(f"{BASE_URL}/cgi-bin/pages/statusview.cgi", cookies=cookies)

    return r.text


def _diagnostic_request(post_url, response_url, data):
    if not logged_in:
        raise ValueError("Must login")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    requests.post(post_url, headers=headers, cookies=cookies, data=data)

    sleep(1)

    r = requests.get(response_url, cookies=cookies)

    return r.text


def diagnostic_ping_html(target, type_id):
    if not target:
        raise ValueError("Must provide target")

    if not type_id:
        raise ValueError("Must provide type")

    print(f":: Making diagnostic 'ping' request for '{target}'")

    return _diagnostic_request(f"{BASE_URL}/cgi-bin/pages/maintenance/disagnostic/ping.asp",
                               f"{BASE_URL}/cgi-bin/pages/maintenance/disagnostic/DiagGeneral.cgi?1",
                               f"wanPVCFlag=0&PINGFlag={type_id}&pingIPAddr={target}")


def diagnostic_dsl_html(type_id):
    if not type_id:
        raise ValueError("Must provide type")

    print(f":: Making diagnostic 'dsl' request'")

    return _diagnostic_request(f"{BASE_URL}/cgi-bin/pages/maintenance/disagnostic/dslLine.asp",
                               f"{BASE_URL}/cgi-bin/pages/maintenance/disagnostic/DiagGeneral.cgi?2",
                               f"wanPVCFlag=0&DSLFlag={type_id}")

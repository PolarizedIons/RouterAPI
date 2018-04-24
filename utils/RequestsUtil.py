import base64

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

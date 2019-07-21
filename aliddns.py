#!/usr/bin/python3

import base64
import hmac
import json
import re
import sys
import urllib.request
from urllib.parse import quote
from _sha1 import sha1
import time
from datetime import datetime
import sys
import os




aliddnsipv6_ak = "AccessKeyId"
aliddnsipv6_sk = "Access Key Secret"
aliddnsipv6_name1 = 'subDomainName'
aliddnsipv6_domain = 'domainName'
aliddnsipv6_ttl = "600"

timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 8 * 60 * 60))
timestamp = timestamp.replace(":", "%3A")

if aliddnsipv6_name1 == "@":
    aliddnsipv6_name = aliddnsipv6_domain
else:
    aliddnsipv6_name = aliddnsipv6_name1 + "." + aliddnsipv6_domain


def format_param(action):
    D = {
        'AccessKeyId': aliddnsipv6_ak,
        'Action': action,
        'Format': 'JSON',
        'Version': '2015-01-09'
    }

    sortedD = sorted(D.items(), key=lambda x: x[0])
    # url_sortedD=percentEncode(sortedD)
    canstring = ''
    # for k, v in sortedD:
    #     canstring += '&' + percentEncode(k) + '=' + percentEncode(v)
    stringToSign = 'GET&%2F&' + percentEncode(canstring[1:])
    # access_key_secret = 'access_key_secret'
    h = hmac.new(bytes(aliddnsipv6_sk + "&", encoding="utf8"), bytes(stringToSign, encoding="utf8"), sha1)
    signature = base64.encodebytes(h.digest()).strip()
    return str(signature, encoding="utf8")


def percentEncode(str):
    res = quote(str, 'utf8')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def get_Local_ipv6_address_win():
    """
	Get local ipv6
    """
    # pageURL = 'https://ip.zxinc.org/ipquery/'
    # pageURL = 'https://ip.sb/'
    pageURL = 'https://api-ipv6.ip.sb/ip'
    content = urllib.request.urlopen(pageURL).read()
    webContent = content.decode("utf8")

    print(webContent)
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, webContent)

    if m is not None:
        return m.group()
    else:
        return None


def get_Local_ipv6_address_linux():
    """
	Get local ipv6
    """
    # pageURL = 'https://ip.zxinc.org/ipquery/'
    # pageURL = 'https://ip.sb/'
    linelist = os.popen(
        ''' ip addr show eth0 | grep "inet6.*global" | awk \'{print $2}\' | awk -F"/" \'{print $1}\' ''').readlines()  # 这个返回值是一个list
    if linelist:
        content = linelist[0].strip()
    else:
        return None
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, content)

    if m is not None:
        return m.group()
    else:
        return None


def send_request(action, urlParam):
    args = "AccessKeyId=" + aliddnsipv6_ak + "&Action=" + action + "&Format=json&" + urlParam + "&Version=2015-01-09"
    # signStr = "AccessKeyId=" + aliddnsipv6_ak + "&Action=" + action + "&Format=json&"+urlParam+"&Version=2015-01-09"
    signStr = "GET&%2F&" + percentEncode(args)
    h = hmac.new(bytes(aliddnsipv6_sk + "&", encoding="utf8"), bytes(signStr, encoding="utf8"), sha1)
    signature = base64.encodebytes(h.digest()).strip()

    url = "https://alidns.aliyuncs.com/?" + args + "&Signature=" + str(signature, encoding="utf8")
    jsonStr = urllib.request.urlopen(url).read().decode("utf8")
    return jsonStr


def get_record_id():
    # signature =
    urlParam = "SignatureMethod=HMAC-SHA1&SignatureNonce=" + timestamp + "&SignatureVersion=1.0&SubDomain=" + aliddnsipv6_name + "&Timestamp=" + timestamp + "&Type=AAAA"
    jsonStr = send_request("DescribeSubDomainRecords", urlParam)
    jsonD = json.loads(jsonStr)
    try:
        recordid = jsonD["DomainRecords"]["Record"][0]["RecordId"]
        return recordid
    except Exception:
        return ""


def get_record_info():
    # signature =
    urlParam = "SignatureMethod=HMAC-SHA1&SignatureNonce=" + timestamp + "&SignatureVersion=1.0&SubDomain=" + aliddnsipv6_name + "&Timestamp=" + timestamp + "&Type=AAAA"
    jsonStr = send_request("DescribeSubDomainRecords", urlParam)
    jsonD = json.loads(jsonStr)
    try:
        # recordid = jsonD["DomainRecords"]["Record"][0]["RecordId"]
        return jsonD
    except Exception:
        return ""


def update_record(recordId, ipv6addr):
    # send_request "UpdateDomainRecord" "RR=$aliddnsipv6_name1&RecordId=$1&SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&TTL=$aliddnsipv6_ttl&Timestamp=$timestamp&Type=AAAA&Value=$(enc $ipv6)"
    urlParam = "RR=" + aliddnsipv6_name1 + "&RecordId=" + recordId + "&SignatureMethod=HMAC-SHA1&SignatureNonce=" + timestamp + "&SignatureVersion=1.0&TTL=" + aliddnsipv6_ttl + "&Timestamp=" + timestamp + "&Type=AAAA&Value=" + percentEncode(
        ipv6addr)
    send_request("UpdateDomainRecord", urlParam)


def add_record(ipv6addr):
    # send_request "AddDomainRecord&DomainName=$aliddnsipv6_domain" "RR=$aliddnsipv6_name1&SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&TTL=$aliddnsipv6_ttl&Timestamp=$timestamp&Type=AAAA&Value=$(enc $ipv6)"
    urlParam = "RR=" + aliddnsipv6_name1 + "&SignatureMethod=HMAC-SHA1&SignatureNonce=" + timestamp + "&SignatureVersion=1.0&TTL=" + aliddnsipv6_ttl + "&Timestamp=" + timestamp + "&Type=AAAA&Value=" + percentEncode(
        ipv6addr)
    send_request("AddDomainRecord&DomainName=" + aliddnsipv6_domain, urlParam)


if __name__ == '__main__':
    sysPlatform = sys.platform
    ipv6Addr=""
    if sysPlatform == "linux":
        ipv6Addr = get_Local_ipv6_address_linux()
        print()
    elif sysPlatform == "win32":
        ipv6Addr = get_Local_ipv6_address_win()
        # print()
    else:
        ipv6Addr = get_Local_ipv6_address_win()

    if not ipv6Addr:
        exit()
    # ipv6Addr = "2409:8a20:c1a:6cf0:dde6:f32:2017:ba95"
    print(ipv6Addr)

    # recordid = get_record_id()
    jsonD = get_record_info()
    recordid = jsonD["DomainRecords"]["Record"][0]["RecordId"]
    if recordid == "":
        add_record(ipv6Addr)
    else:
        ipvalue = jsonD["DomainRecords"]["Record"][0]["Value"]
        if ipvalue != ipv6Addr:
            update_record(recordid, ipv6Addr)

from mitmproxy.script import concurrent
import pcrclient
import json
from os.path import dirname, join, exists
import os
from shutil import copy
import datetime

curpath = dirname(__file__)


def forma(url):
    url = url.split('net')[-1][1:]
    url = url.replace('/', '-')
    return url


def process(content, url, typ):
    if any(x in url for x in ["/pool/Movie", "client_ob", "domain_switch_count", "/media/", "/sdk-hot-deploy/", "/webstatic/"]):
        print(f'skipping {url[:256]}')
        return
    try:
        unpacked = ({}, "") if len(content) == 0 else (pcrclient.pcrclient.unpackRsp(content) if typ == "response" else pcrclient.pcrclient.unpack(content))
    except Exception as e:
        return
        print(f'    Exception occurred on unpacking: {repr(e)[:256]}')
    print(f'\n{url[:256]} {typ}')
    print(f'    {str(unpacked)[:256]} {"..." if len(unpacked) > 256 else ""}')
    if not os.path.exists(join(curpath, "debug")):
        os.makedirs(join(curpath, "debug"))
    path = join(curpath, f'debug/{str(forma(url))[:128]}.json')
    dic = {}
    if exists(path):
        try:
            with open(path, 'r', encoding="utf-8") as fp:
                dic = json.load(fp)
        except Exception as e:
            print(f'Failed to load {path}: {e}')
            dic = {}
    try:
        with open(path, 'w', encoding="utf-8") as fp:
            dic["time"] = f'{datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")}'
            dic["url"] = url
            dic[f'{typ}'] = unpacked[0]
            json.dump(dic, fp, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'    Exception occurred on dumping: {repr(e)[:256]}')
        return

    with open(join(curpath, "log.txt"), "a+", encoding="utf-8") as fp:
        if typ != "response":
            print(f'{datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")}  {url.split("net")[-1][1:]} {typ}', file=fp, end=" ")
        else:
            print(typ, file=fp)
            if not os.path.exists(join(curpath, "last10")):
                os.makedirs(join(curpath, "last10"))
            filenames = list(sorted(os.listdir(join(curpath, "last10")), reverse=True))
            for filename in filenames:
                if filename[0] in ['_', '9']:
                    os.remove(join(curpath, f'last10/{filename}'))
                elif 0 <= int(filename[0]) < 9:
                    os.rename(join(curpath, f'last10/{filename}'), join(curpath, f'last10/{int(filename[0])+1}{filename[1:]}'))
            copy(path, join(curpath, f'last10/0_{str(forma(url))[:128]}.json'))
            copy(path, join(curpath, 'last10/_.json'))


@concurrent
def request(flow):
    if "biligame.net" not in flow.request.url:
        return
    if "/api/" in flow.request.url or "/app/" in flow.request.url:
        return
    process(flow.request.content, flow.request.url, "request")


@concurrent
def response(flow):
    if "biligame.net" not in flow.request.url:
        return
    if "/api/" in flow.request.url or "/app/" in flow.request.url:
        return
    process(flow.response.content, flow.request.url, "response")

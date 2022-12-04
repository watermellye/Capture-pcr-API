from mitmproxy.script import concurrent
import pcrclient
import json
from os.path import dirname, join, exists
import datetime

curpath = dirname(__file__)


def forma(url):
    url = url.split('net')[-1][1:]
    url = url.replace('/', '-')
    return url


def process(content, url, typ):
    try:
        print(f'\n           Raw Data: {typ}\n           url={url[:256]}\n           content_short={str(content)[:100]}')
        unpacked = pcrclient.pcrclient.unpackRsp(content) if typ == "response" else pcrclient.pcrclient.unpack(content)
        print(f'           content_decoded_short={str(unpacked)[:100]}\n')
    except Exception as e:
        re = repr(e)
        print(f'\n           Exception occurred in unpacking ({typ})')
        print(f'\n           {re if len(re) <= 100 else re[:50] + " ...... " + re[:-50]}\n')
    else:
        path = join(curpath, "debug/", f'{str(forma(url))[:256]}.json')
        dic = {}
        if exists(path):
            with open(path, 'r', encoding="utf-8") as fp:
                dic = json.load(fp)
        try:
            with open(path, 'w', encoding="utf-8") as fp:
                dic["time"] = f'{datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")}'
                dic["url"] = url
                dic[f'{typ}'] = unpacked[0]
                json.dump(dic, fp, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'\n           Exception occurred in dumping ({typ})\n           {repr(e)}\n')
        with open(join(curpath, "log.txt"), "a+", encoding="utf-8") as fp:
            if typ != "response":
                print(f'{datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")}  {url.split("net")[-1][1:]} {typ}', file=fp, end=" ")
            else:
                print(f'{typ}', file=fp)


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

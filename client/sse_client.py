import re
import json

import requests

def _check_evensource(b):
    re_obj = re.compile(r"^(data: (.*)\n\n).*")
    buf_s = "".join(b)
    m = re_obj.match(buf_s)
    if not m:
        return b, False

    b = b[m.end(1):]

    return b, m.group(2)


def iter_content(resp):
    """
    Iterates over a requests.Response object
    and return event source data

    :param resp:
    :return:
    """
    buf = []


    for d in resp.iter_content(chunk_size=1):
        buf.append(d)
        buf, m = _check_evensource(buf)
        if m:
            yield m


def iter_json(resp):
    for d in iter_content(resp):
        yield json.loads(d)


if __name__ == "__main__":
    r = requests.get("http://localhost:9191/event/sse_data", stream=True)
    print "EVENT_DATA : "
    for d in iter_content(r):
        print d

    print "EVENT_JSON_DATA : "
    r = requests.get("http://localhost:9191/event/sse_json", stream=True)
    for d in iter_json(r):
        print d




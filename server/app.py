#!/usr/bin/env python

import json

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import jinja2.debug

gevent.monkey.patch_all()

from flask import Flask, request, Response


app = Flask(__name__)

def sse(data):
    return 'data: %s\n\n' % data

def sse_data():
    count = 0
    while count < 10:
        gevent.sleep(1)
        yield sse(count)
        count += 1


def sse_json():
    count = 0
    while count < 10:
        gevent.sleep(1)
        yield sse(json.dumps({"success":True, "data":count}))
        count += 1


event_handlers = {
    "sse_data":sse_data,
    "sse_json":sse_json
}


@app.route('/event/<event_name>')
def sse_request(event_name):
    return Response(
        event_handlers[event_name](),
        mimetype='text/event-stream')


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 9191), app)
    http_server.serve_forever()

    #app.run(host='127.0.0.1', port=9191, debug=True)

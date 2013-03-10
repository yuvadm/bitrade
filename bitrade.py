# encoding: utf8
import json
import logging
import os

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import tornadoredis

from time import time
from uuid import uuid4

c = tornadoredis.Client()
c.connect()


class Order(object):
    def __init__(self, data):
        self.id = uuid4().hex
        self.time = str(int(time() * 1000))  # ms resolution
        for key in data:
            setattr(self, key, data[key])

    def __unicode__(self):
        return json.dumps(self.__dict__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title='OHAI BITRADE SERVER')


class OrderHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(OrderHandler, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'test_channel')
        self.client.listen(self.on_order)

    @tornado.gen.engine
    def on_message(self, msg):
        order = Order(json.loads(msg))
        with c.pipeline() as pipe:
            order_str = unicode(order)
            pipe.zadd('order_log', order.time, order_str)
            pipe.publish('test_channel', order_str)
            yield tornado.gen.Task(pipe.execute)

    def on_order(self, msg):
        if msg.kind == 'message':
            self.write_message(str(msg.body))

    def close(self):
        self.client.unsubscribe('test_channel')
        self.client.disconnect()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/orders', OrderHandler),
        ]
        settings = dict(
            debug=True,
            # template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            # static_path=os.path.join(os.path.dirname(__file__), 'static'),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9000)
    print('B⃦ Bitrade server running... (Ctrl-C to stop)')
    tornado.ioloop.IOLoop.instance().start()

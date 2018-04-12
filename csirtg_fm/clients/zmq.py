import os.path
import zmq
from pprint import pprint

TYPE = os.environ.get('CSIRTG_FM_ZMQ_TYPE', 'PUB')
TOPIC = os.environ.get('CSIRTG_FM_ZMQ_TOPIC', 'scanners')
ENDPOINT = os.environ.get('CSIRTG_FM_ZMQ_ENDPOINT', 'ipc:///tmp/csirtg_fm.ipc')

TYPE_MAPPING = {
    'PUB': zmq.PUB,
    'PUSH': zmq.PUSH,
    'PUSH_ZYRE_GATEWAY': zmq.DEALER,
}


class _Zmq(object):

    __name__ = 'zmq'

    def __init__(self, socket_type=TYPE, topic=TOPIC, endpoint=ENDPOINT):
        self.socket_type = socket_type
        self.topic = topic
        self.endpoint = endpoint
        if not endpoint:
            raise ValueError("Invalid endpoint: '{}'".format(endpoint))

        context = zmq.Context()
        self.socket = context.socket(TYPE_MAPPING[socket_type])
        self.socket.connect(self.endpoint)

    def ping(self):
        return True

    def indicators_create(self, data):

        data = [data]

        if self.socket_type == "PUB":
            for i in data:
                self.socket.send_multipart([self.topic, str(i)])
            return

        if self.socket_type == 'PUSH_ZYRE_GATEWAY':
            for i in data:
                self.socket.send_multipart(['PUB', self.topic, str(i)])
            return

        for i in data:
            self.socket.send(str(i))


Plugin = _Zmq


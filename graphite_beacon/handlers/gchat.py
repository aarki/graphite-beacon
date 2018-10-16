import json

from tornado import httpclient as hc
from tornado import gen

from graphite_beacon.handlers import LOGGER, AbstractHandler
from graphite_beacon.template import TEMPLATES


class GChatHandler(AbstractHandler):

    name = 'gchat'

    # Default options
    defaults = {
        'webhook': None,
    }

    def init_handler(self):
        self.webhook = self.options.get('webhook')
        assert self.webhook, 'GChat webhook is not defined.'
        self.client = hc.AsyncHTTPClient()

    def get_message(self, level, alert, value, target=None, ntype=None):  # pylint: disable=unused-argument
        msg_type = 'gchat' if ntype == 'graphite' else 'short'
        tmpl = TEMPLATES[ntype][msg_type]
        return tmpl.generate(
            level=level, reactor=self.reactor, alert=alert, value=value, target=target).strip()

    @gen.coroutine
    def notify(self, level, *args, **kwargs):
        LOGGER.debug("Handler (%s) %s", self.name, level)

        message = self.get_short(level, *args, **kwargs).decode('UTF-8')
        data = {'text': message}

        body = json.dumps(data)
        yield self.client.fetch(
            self.webhook,
            method='POST',
            headers={'Content-Type': 'application/json'},
            body=body
        )

import json
from datetime import datetime

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

    def get_short(self, level, alert, value, target=None, ntype=None, rule=None):  # pylint: disable=unused-argument
        tmpl = TEMPLATES[ntype]['gchat']
        return tmpl.generate(
            level=level, reactor=self.reactor, alert=alert, value=value, target=target).strip()

    @gen.coroutine
    def notify(self, level, *args, **kwargs):
        LOGGER.debug("Handler (%s) %s", self.name, level)

        message = self.get_short(level, *args, **kwargs).decode('UTF-8')
        data = {'text': message}

        webhook = self.webhook.replace('{{CURRENT_DAY}}', datetime.utcnow().strftime("%Y%m%d"))

        body = json.dumps(data)
        yield self.client.fetch(
            webhook,
            method='POST',
            headers={'Content-Type': 'application/json; charset=UTF-8'},
            body=body
        )

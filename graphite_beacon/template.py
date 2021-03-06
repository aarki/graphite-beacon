import os.path as op

from tornado import template

LOADER = template.Loader(op.join(op.dirname(op.abspath(__file__)), 'templates'), autoescape=None)
TEMPLATES = {
    'graphite': {
        'html': LOADER.load('graphite/message.html'),
        'text': LOADER.load('graphite/message.txt'),
        'short': LOADER.load('graphite/short.txt'),
        'subject': LOADER.load('graphite/subject.txt'),
        'telegram': LOADER.load('graphite/short.txt'),
        'slack': LOADER.load('graphite/slack.txt'),
        'gchat': LOADER.load('graphite/gchat.txt'),
    },
    'url': {
        'html': LOADER.load('url/message.html'),
        'text': LOADER.load('url/message.txt'),
        'short': LOADER.load('url/short.txt'),
        'subject': LOADER.load('url/subject.txt'),
        'gchat': LOADER.load('graphite/gchat.txt'),
    },
    'common': {
        'html': LOADER.load('common/message.html'),
        'text': LOADER.load('common/message.txt'),
        'short': LOADER.load('common/short.txt'),
        'subject': LOADER.load('common/subject.txt'),
        'gchat': LOADER.load('graphite/gchat.txt'),
    },
}

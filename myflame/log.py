import logging

log = logging.getLogger("werkzeug")


def e():
    print('ded')


log.addHandler(e)
log.setLevel(logging.DEBUG)
print(log.hand1le(e))
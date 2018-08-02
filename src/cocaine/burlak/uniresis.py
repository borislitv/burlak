'''Uniresis service proxy

Used mostly for debug purposes as a stub, until real uniresis would
be available.

Remove candidate.
'''

from cocaine.services import Service

from tornado import gen


class ResoursesProxy(object):
    @gen.coroutine
    def uuid(self):  # pragma: no cover
        raise NotImplementedError(
            'uuid method sould be defined in derived classes'
        )

    @gen.coroutine
    def extra(self):
        raise NotImplementedError(
            'extra method sould be defined in derived classes'
        )


class UniresisProxy(ResoursesProxy):

    def __init__(self, context, endpoints, name):
        self.config = context.config

        self.name = name
        self.uniresis = \
            Service(name, endpoints) if endpoints else Service(name)

    @property
    def service_name(self):
        """Return name of backend service.

        Shoud return either 'locator' or 'uniresis'.

        """
        return self.name

    @gen.coroutine
    def uuid(self):
        """Resquest uuid from uniresis service."""
        ch = yield self.uniresis.uuid()
        uuid = yield ch.rx.get(timeout=self.config.api_timeout)

        raise gen.Return(uuid)

    @gen.coroutine
    def extra(self):
        """Resquest extra records from uniresis/locator service.

        Cluster name of main intrest in 'extra' json.

        """
        ch = yield self.uniresis.extra()
        extra = yield ch.rx.get(timeout=self.config.api_timeout)

        raise gen.Return(extra)


class DummyProxy():
    '''Stub for resource proxy
    Used for local tests purposes
    '''

    COCAINE_TEST_UUID = 'SOME_UUID'
    TEST_TAG = '_test_tag'

    def __init__(self, uuid=None, tag=None):
        self._uuid = uuid if uuid else DummyProxy.COCAINE_TEST_UUID
        self._tag = tag if tag else DummyProxy.TEST_TAG

    @property
    def service_name(self):
        return 'dumm_proxy'

    @gen.coroutine
    def uuid(self):
        raise gen.Return(self._uuid)

    @gen.coroutine
    def extra(self):
        raise gen.Return(self._tag)


def catchup_an_uniresis(
        context, use_stub_uuid=None, endpoints=None, service_name='uniresis'):
    """Construct uniresis proxy.

    Note that `service_name` must be locator, uniresis will be deprecated
    someday.
    """
    if use_stub_uuid:
        return DummyProxy(use_stub_uuid)
    else:
        return UniresisProxy(context, endpoints, service_name)

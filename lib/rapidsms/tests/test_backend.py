#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import unittest
import rapidsms.backends


class MockRouter(object):
    def __init__(self):
        self.messages = []
    
    def receive(self, message):
        self.messages.append(message)


class TestBackend(unittest.TestCase):

    REQUIRED_METHODS = ("start", "stop", "send", "receive")

    def setUp(self):
        self.mock_router = MockRouter()
        self.backend = rapidsms.backends.Spomc(self.mock_router)
    
    def tearDown(self):
        pass
    
    def test_api(self):
        for m in self.REQUIRED_METHODS:
            base_method = getattr(self.backend.super, m)
            backend_method = getattr(self.backend, m)
            self.assertTrue(base_method != backend_method, 
                "Missing method: %s" % (m))

    def test_notifies_router(self):
        n = len(self.mock_router.messages)
        self.backend.receive("1234", "Test Message")
        self.assertTrue(len(self.mock_router.messages) > n,
            "The backend didn't notify it's router of an incoming message")
    
    # things to test:
    #   sending messages (without *really* doing it)
    #   arity of api methods (use inspect.getargspec)
    #   individual tests for required API methods


if __name__ == "__main__":
    unittest.main()
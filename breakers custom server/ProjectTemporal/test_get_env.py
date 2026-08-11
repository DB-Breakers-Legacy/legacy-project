from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse
import msgpack

class HappyPathGetEnvTest(TestCase):
    def test_basic(self):
        uri = reverse('getEnv', args=['a', 'b'])
        response = self.client.post(uri)
        data = msgpack.unpackb(response.content, raw=False)
        a, b = data
        self.assertEqual(a['result'], 0)

from django.test import TestCase
from .models import Share
from .models import Commodity


class ShareTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our Product models """

    def test_str(self):
        test_name = Share(name='A share')
        self.assertEqual(str(test_name), 'A share')

class CommodityTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our Product models """

    def test_str(self):
        test_name = Commodity(name='A commodity')
        self.assertEqual(str(test_name), 'A commodity')
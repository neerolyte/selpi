from unittest import TestCase, skip
from muster import Muster
from unittest_data_provider import data_provider
from unittest.mock import Mock
import variable

class MusterTest(TestCase):
    def test_query(self):
        protocol = Mock()
        protocol.query.side_effect = [b'\x12\x34', b'\x56\x78']
        muster = Muster(protocol)
        ivars = [
            variable.create('CommonScaleForAcVolts'),
            variable.create('CommonScaleForTemperature'),
        ]
        rvars = muster.query(ivars)
        self.assertEqual(2, len(ivars))
        self.assertEqual('CommonScaleForAcVolts', rvars[0].get_name())
        self.assertEqual('CommonScaleForTemperature', rvars[1].get_name())
        self.assertEqual(b'\x12\x34', rvars[0].get_bytes())
        self.assertEqual(b'\x56\x78', rvars[1].get_bytes())
        self.assertEqual((41000, 0), protocol.query.call_args_list[0].args)
        self.assertEqual((41004, 0), protocol.query.call_args_list[1].args)

from unittest import TestCase, skip
from unittest.mock import Mock, call
from muster import Muster
from unittest_data_provider import data_provider
import variable

class MusterTest(TestCase):
    def test_update(self):
        protocol = Mock()
        protocol.query.side_effect = [b'\x12\x34\x00\x00\x00\x00\x00\x00\x56\x78']
        muster = Muster(protocol)
        vars = [
            variable.create('CommonScaleForAcVolts'),
            variable.create('CommonScaleForTemperature'),
        ]

        muster.update(vars)

        self.assertEqual(2, len(vars))
        self.assertEqual('CommonScaleForAcVolts', vars[0].get_name())
        self.assertEqual('CommonScaleForTemperature', vars[1].get_name())
        self.assertEqual(b'\x12\x34', vars[0].bytes)
        self.assertEqual(b'\x56\x78', vars[1].bytes)
        self.assertEqual(1, len(protocol.query.call_args_list))
        self.assertEqual(call(41000, 4), protocol.query.call_args_list[0])

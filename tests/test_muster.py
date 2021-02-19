from unittest import TestCase, skip
from unittest.mock import call, create_autospec
from muster import Muster
from unittest_data_provider import data_provider
from memory import Protocol, Range, variable

class MusterTest(TestCase):
    def test_update(self):
        protocol = create_autospec(Protocol)
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
        self.assertEqual(call(Range(41000, 5)), protocol.query.call_args_list[0])

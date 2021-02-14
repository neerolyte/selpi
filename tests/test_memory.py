from unittest import TestCase, skip
import memory
from unittest_data_provider import data_provider

class ProtocolTest(TestCase):
    @data_provider(lambda: (
        ("CommonScaleForAcVolts", "ushort"),
        ("ACLoadkWhTotalAcc", "uint"),
    ))
    def test_get_type(self, name, expected):
        self.assertEqual(memory.get_type(name), expected)

    @data_provider(lambda: (
        ("CommonScaleForAcCurrent", 41001),
        ("BatteryVolts", 41052),
    ))
    def test_get_address(self, name, expected):
        self.assertEqual(memory.get_address(name), expected)

    @data_provider(lambda: (
        ("CommonScaleForDcVolts", None),
        ("TotalKacokWhTotalAcc", "Wh"),
    ))
    def test_get_units(self, name, expected):
        self.assertEqual(memory.get_units(name), expected)

    @data_provider(lambda: (
        # ('MemoryName', bytes, expected)
        ('CommonScaleForDcVolts', b'\x1a\x04', 1050),
        ('CommonScaleForTemperature', b'\x12\x02', 530),
        ('Shunt1Power', b'\x46\xfe', -1699.5849609375),
        ('Shunt1Power', b'\x3f\xfe', -1726.50146484375),
        ('Shunt1Power', b'\x7a\xfe', -1499.6337890625),
        ('Shunt1Power', b'\xfd\xff', -11.53564453125),
        ('BatteryVolts', b'\x41\x44', 55.989532470703125),
        ('BatteryVolts', b'\x3a\x44', 55.96710205078125),
        ('BatteryTemperature', b'\x44\x05', 21.802978515625),
        ('LoadAcPower', b'\xff\x02\x00\x00', 341.1567687988281),
        ('LoadAcPower', b'\x1d\x03\x00\x00', 354.5005798339844),
        ('DCBatteryPower', b'\xd4\xff\xff\xff', -169.189453125),
        ('DCBatteryPower', b'\xf4\xff\xff\xff', -46.142578125),
        ('ACLoadkWhTotalAcc', b'\x19\xeb\x00\x00', 5139822.509765625),
        ('BattOutkWhPreviousAcc', b'\x29\x00\x00\x00', 3783.69140625),
        ('BattSocPercent', b'\xdb\x63', 99.85546875),
        ('Shunt1Name', b'\x01\x00', 'Solar'),
        ('Shunt2Name', b'\x00\x00', 'None'),
        ('Shunt1Name', b'\x3a\x00', 'Error'),
    ))
    def test_scale(self, name, bytes, expected):
        scales = {
            'CommonScaleForDcVolts': 1050,
            'CommonScaleForDcCurrent': 12000,
            'CommonScaleForTemperature': 530,
            'CommonScaleForAcVolts': 5300,
            'CommonScaleForAcCurrent': 2200,
        }
        self.assertEqual(memory.scale(name, bytes, scales), expected)

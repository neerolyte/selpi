from unittest import TestCase, skip
import variable
from variable import Variable
from unittest_data_provider import data_provider
from error import Error
from memory_range import Range

scales = {
    'CommonScaleForDcVolts': 1050,
    'CommonScaleForDcCurrent': 12000,
    'CommonScaleForTemperature': 530,
    'CommonScaleForAcVolts': 5300,
    'CommonScaleForAcCurrent': 2200,
}

class VariableTest(TestCase):
    @data_provider(lambda: (
        # (arg, name, address)
        ('CommonScaleForDcVolts', 'CommonScaleForDcVolts', 0xa02a),
        ('Shunt1Power', 'Shunt1Power', 0xa088),
        ('BatteryVolts', 'BatteryVolts', 0xa05c),
        ('BattSocPercent', 'BattSocPercent', 0xa081),

        (0xa02a, 'CommonScaleForDcVolts', 0xa02a),
        (0xa088, 'Shunt1Power', 0xa088),
        (0xa05c, 'BatteryVolts', 0xa05c),
        (0xa081, 'BattSocPercent', 0xa081),

        (0xcafe, 'Unknown', 0xcafe),
        (0xfeed, 'Unknown', 0xfeed),
    ))
    def test_create(self, arg, name, address):
        var = variable.create(arg)
        self.assertIsInstance(var, variable.Variable)
        self.assertEqual(address, var.range.address)
        self.assertEqual(name, var.get_name())

    @data_provider(lambda: (
        ('CommonScaleForDcVolts', Range(41002, 1)),
        ('BattOutkWhPreviousAcc', Range(41356, 2)),
        ('DCBatteryPower', Range(41007, 2)),
        (0xcafe, Range(0xcafe, 1)),
        (0xfeed, Range(0xfeed, 1)),
    ))
    def test_range(self, arg, range):
        self.assertEqual(range, variable.create(arg).range)

    @data_provider(lambda: (
        # (arg, type)
        ('CommonScaleForDcVolts', 'ushort'),
        ('BattOutkWhPreviousAcc', 'uint'),
        ('DCBatteryPower', 'int'),
        (0xcafe, 'ushort'),
        (0xfeed, 'ushort'),
    ))
    def test_get_type(self, arg, type):
        self.assertEqual(type, variable.create(arg).get_type())

    @data_provider(lambda: (
        ('CommonScaleForDcVolts', b'\x1a\x04', 1050),
        ('BatteryVolts', b'\x41\x44', 55.989532470703125),
    ))
    def test_set_bytes(self, arg, bytes, value):
        var = variable.create(arg)
        ovalue = var.get_value(scales)
        nvar = var.set_bytes(bytes)
        self.assertEqual(ovalue, var.get_value(scales))
        self.assertEqual(value, nvar.get_value(scales))

    @data_provider(lambda: (
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
    def test_get_value(self, name, bytes, value):
        address = 0xcafe # address doesn't matter for this test
        var = Variable(name, address, bytes)
        self.assertEqual(value, var.get_value(scales))

    def test_get_value_errors(self):
        var = variable.create(0xcafe)
        with self.assertRaises(Error) as context:
            var.get_value([])
        self.assertEqual(
            'Can not convert value for unknown variable type',
            context.exception.args[0]
        )

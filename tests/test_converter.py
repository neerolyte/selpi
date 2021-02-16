from unittest import TestCase, skip
from converter import convert
from unittest_data_provider import data_provider

scales = {
    'CommonScaleForDcVolts': 1050,
    'CommonScaleForDcCurrent': 12000,
    'CommonScaleForTemperature': 530,
    'CommonScaleForAcVolts': 5300,
    'CommonScaleForAcCurrent': 2200,
}

class ConverterTest(TestCase):
    @data_provider(lambda: (
        ('ac_w', 797, 354.5005798339844),
        ('ac_w', 767, 341.1567687988281),
        ('ac_wh', 60185, 5139822.509765625),
        ('dc_v', 17466, 55.96710205078125),
        ('dc_v', 17473, 55.989532470703125),
        ('dc_w', -442, -1699.5849609375),
        ('dc_w', -44, -169.189453125),
        ('dc_w', -12, -46.142578125),
        ('dc_w', -3, -11.53564453125),
        ('dc_wh', 41, 3783.69140625),
        ('percent', 25563, 99.85546875),
        ('shunt_name', 0, 'None'),
        ('shunt_name', 1, 'Solar'),
        ('shunt_name', 58, 'Error'),
        ('temperature', 1348, 21.802978515625),
    ))
    def test_convert(self, conversion, bytes, value):
        self.assertEqual(value, convert(conversion, bytes, scales))

from unittest import TestCase
from memory import reduce, Range
from unittest_data_provider import data_provider

class ReduceTest(TestCase):
    @data_provider(lambda: (
        (
            [
                Range(0x1234, 2),
            ],
            [
                Range(0x1234, 2),
            ]
        ),
        (
            [
                Range(0x0010, 1),
                Range(0x0014, 2),
            ],
            [
                Range(0x0010, 6),
            ]
        ),
        (
            [
                Range(0x0004, 2),
                Range(0x0000, 1),
            ],
            [
                Range(0x0000, 6),
            ]
        ),
        (
            [
                Range(0x0001, 2),
                Range(0x0002, 2),
                Range(0x0003, 2),
            ],
            [
                Range(0x0001, 4),
            ]
        ),
        # Split across MAX_WORDS (256)
        (
            [
                Range(0x0000, 2),
                Range(0x00ff, 1),
                Range(0x0103, 1),
                Range(0x0203, 1),
                Range(0x0301, 2),
            ],
            [
                Range(0x0000, 256),
                Range(0x0103, 1),
                Range(0x0203, 256),
            ]
        ),
    ))
    def test_reduce(self, ranges, expected):
        self.assertEqual(expected, reduce(ranges))

from unittest import TestCase, skip
from memory_range import Range, combine
from variable import Variable
from unittest_data_provider import data_provider
from error import Error

class MemoryRangeTest(TestCase):
    @data_provider(lambda: (
        (Range(0x0000, 3), Range(0x0000, 3), True),
        (Range(0x0000, 3), Range(0x0000, 4), False),
        (Range(0xa033, 1), Range(0xa033, 1), True),
        (Range(0xa033, 1), Range(0xa034, 1), False),
        (Range(0xa033, 1), [Range(0xa033, 1)], False),
    ))
    def test___eq__(self, r1, r2, expected):
        self.assertEqual(expected, r1 == r2)

    @data_provider(lambda: (
        (Range(0x0000, 3), 'Range(0x0000, 3)'),
        (Range(0x1234, 99), 'Range(0x1234, 99)'),
        (Range(0xcafe, 1), 'Range(0xcafe, 1)'),
    ))
    def test___repr__(self, range, expected):
        self.assertEqual(expected, repr(range))

    @data_provider(lambda: (
        (
            [
                Range(0x0000, 2),
                Range(0x0004, 3),
            ],
            [
                Range(0x0000, 2),
                Range(0x0004, 3),
            ]
        ),
        (
            [
                Range(0x0009, 1),
                Range(0x0004, 3),
                Range(0x0000, 2),
                Range(0x0007, 1),
            ],
            [
                Range(0x0000, 2),
                Range(0x0004, 3),
                Range(0x0007, 1),
                Range(0x0009, 1),
            ]
        ),
    ))
    def test_sorted(self, ranges, expected):
        self.assertEqual(expected, sorted(ranges))


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
    def test_combine(self, ranges, expected):
        self.assertEqual(expected, combine(ranges))

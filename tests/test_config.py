import unittest

from config import Config

class ConfigTest(unittest.TestCase):
    def testDefaultPort(self):
        self.assertEqual("/dev/ttyUSB0", Config().get("port"))

    def testDefaultPassword(self):
        self.assertEqual("Selectronic SP PRO", Config().get("password"))

if __name__ == '__main__':
    unittest.main() 

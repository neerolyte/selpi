import unittest

import config

class ConfigTest(unittest.TestCase): 
    def testDefaultPort(self):
        self.assertEqual("/dev/ttyUSB0", config.get("port"))

    def testDefaultPassword(self):
        self.assertEqual("Selectronic SP PRO", config.get("password"))

if __name__ == '__main__': 
    unittest.main() 
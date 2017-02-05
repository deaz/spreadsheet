#!/usr/bin/env python3

import unittest

loader = unittest.TestLoader()

suite = loader.discover(start_dir='.', pattern='test_*.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

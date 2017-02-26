import unittest
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
import tetris

class TestTetris(unittest.TestCase):
  def testHello():
    self.assertEqual(6, 7)

import unittest
from fuzzyminerpk import Utility


class TestFuzzyMethods(unittest.TestCase):

    def test_is_valid_matrix1D(self):
        self.d = [1, 2, 3]
        Utility.is_valid_matrix1D(self.d)

    def test_is_valid_matrix2D(self):
        self.d = a = [[1, 2, 3], [4, 5, 6]]
        Utility.is_valid_matrix2D(self.d)

    def test_is_standard_key(self):
        self.key = 'concept lifecycle geeks'
        Utility.is_standard_key(self.key)

    def negative_test_is_valid_matrix1D(self):
        self.d = [-1, 2, 3]
        Utility.is_valid_matrix1D(self.d)

    def negative_test_is_valid_matrix2D(self):
        self.d = a = [[-1, 2, 3], [4, 5, 6]]
        Utility.is_valid_matrix2D(self.d)

    def negative_test_is_standard_key(self):
        self.key = 'it is a negative test case'
        Utility.is_standard_key(self.key)

if __name__ == '__main__':
    unittest.main()
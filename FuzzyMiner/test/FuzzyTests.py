import unittest
from fuzzyminerpk import FMUtility


class TestFuzzyMethods(unittest.TestCase):

    def test_is_valid_matrix1D(self):
        self.d = [1, 2, 3]
        FMUtility.is_valid_matrix1D(self.d)

    def test_is_valid_matrix2D(self):
        self.d = a = [[1, 2, 3], [4, 5, 6]]
        FMUtility.is_valid_matrix2D(self.d)

    def test_is_standard_key(self):
        self.key = 'concept lifecycle geeks'
        FMUtility.is_standard_key(self.key)

    def negative_test_is_valid_matrix1D(self):
        self.d = [-1, 2, 3]
        FMUtility.is_valid_matrix1D(self.d)

    def negative_test_is_valid_matrix2D(self):
        self.d = a = [[-1, 2, 3], [4, 5, 6]]
        FMUtility.is_valid_matrix2D(self.d)

    def negative_test_is_standard_key(self):
        self.key = 'it is a negative test case'
        FMUtility.is_standard_key(self.key)

if __name__ == '__main__':
    unittest.main()
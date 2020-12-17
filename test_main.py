from unittest import TestCase

from main import solution_part_1, solution_part_2


class Test(TestCase):
    def test_solution_part_1(self):
        self.assertEqual(solution_part_1("testData.txt"), 112)

    def test_solution_part_2(self):
        self.assertEqual(solution_part_2("testData.txt"), 848)

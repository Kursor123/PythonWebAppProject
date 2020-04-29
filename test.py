import unittest
import app


class LoadingTest(unittest.TestCase):
    def setUp(self):
        self.problems, self.possible_tags = app.load_problems('test_problems.txt')

    def test_problem_size(self):
        self.assertEqual(len(self.problems), 3)

    def test_tags_size(self):
        self.assertEqual(len(self.possible_tags), 5)

    def test_problem_content(self):
        p = app.Problem(5, {'алгебра', 'теория чисел', 'комбинаторика'}, 'Сколько будет 2 + 2?\n')
        matches = 0
        for x in self.problems:
            if x.text == p.text and x.complexity == p.complexity and x.tags == p.tags:
                matches += 1
        if (matches == 0):
            self.fail('Problem is not found')

    def test_tags_content(self):
        self.assertEqual(self.possible_tags, {'алгебра', 'теория чисел', 'чётность',
                                              'комбинаторика', 'алгоритмы'})


if __name__ == '__main__':
    unittest.main()

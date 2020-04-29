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
        self.assertTrue(p in self.problems)

    def test_tags_content(self):
        self.assertEqual(self.possible_tags, {'алгебра', 'теория чисел', 'чётность',
                                              'комбинаторика', 'алгоритмы'})


class SortingTest(unittest.TestCase):
    def setUp(self):
        self.problems = app.load_problems('test_problems.txt')[0]
        self.complexities = app.sort_by_complexity(self.problems)

    def test_complexities(self):
        for i in range(4):
            for problem in self.complexities[i]:
                self.assertTrue(i + 1 <= problem.complexity <= i + 2)


class GeneratingOlympiadTest(unittest.TestCase):
    def setUp(self):
        self.problems = app.load_problems('test_problems_for_olympiad.txt')[0]
        self.olympiad = app.generate_olympiad(self.problems)

    def test_size(self):
        self.assertEqual(len(self.olympiad), 4)

    def test_complexities(self):
        for i in range(4):
            self.assertTrue(i + 1 <= self.olympiad[i].complexity <= i + 2)

    def test_themes(self):
        for i in range(4):
            for j in range(4):
                if i != j:
                    self.assertFalse(self.olympiad[i].tags <= self.olympiad[j].tags)


if __name__ == '__main__':
    unittest.main()

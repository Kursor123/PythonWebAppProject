from flask import Flask, render_template, request, redirect, url_for
import random
from collections import defaultdict

app = Flask(__name__)

#changes
class Problem:
    def __init__(self, complexity, tags, text):
        self.complexity = complexity
        self.tags = tags
        self.text = text

    def __eq__(self, other):
        if not isinstance(other, Problem):
            raise NotImplementedError
        return self.complexity == other.complexity and \
               self.tags == other.tags and self.text == other.text

    def __hash__(self):
        return str.__hash__(self.text)


suitable_problems = set()


def load_problems(filename):
    problems = []
    possible_tags = set()
    with open(filename, 'r') as f:
        i = 0
        complexity = 0
        tags = set()
        text = ''
        for line in f:
            if i % 2 == 0:
                info = line.split(',')
                tags = set(info[0:-1])
                possible_tags = possible_tags.union(tags)
                complexity = int(info[-1])
            else:
                text = line
                problems.append(Problem(complexity, tags, text))
            i += 1
    return (problems, possible_tags)


def sort_by_complexity(problemset):
    complexities = [[], [], [], []]
    for problem in problemset:
        if problem.complexity == 5:
            complexities[3].append(problem)
        elif problem.complexity == 1:
            complexities[0].append(problem)
        else:
            complexities[problem.complexity - 1].append(problem)
            complexities[problem.complexity - 2].append(problem)
    return complexities


def generate_olympiad(problemset):
    assert (len(problemset) >= 4)
    complexities = sort_by_complexity(problemset)
    olympiad = [0, 0, 0, 0]
    olympiad[3] = random.choice(complexities[3])
    banned = set()
    banned.update(olympiad[3].tags)
    for i in range(1, 3).__reversed__():
        ind = random.randint(0, len(complexities[i]) - 1)
        while len(complexities[i]) and complexities[i][ind].tags <= banned:
            complexities[i][ind], complexities[i][-1] = complexities[i][-1], complexities[i][ind]
            complexities.pop()
            ind = random.randint(0, len(complexities[i]) - 1)
        olympiad[i] = complexities[i][ind]
        banned.update(olympiad[i].tags)
    p = random.choice(complexities[0])
    while p == olympiad[1]:
        p = random.choice(complexities[0])
    olympiad[0] = p
    return olympiad


problems, possible_tags = load_problems('problems.txt')

colors = {'алгебра': 'orchid', 'геометрия': 'skyblue',
          'комбинаторика': 'lightgreen', 'теория чисел': 'crimson',
          'игры': 'cyan', 'чётность': 'darkkhaki', 'алгоритмы': 'navy',
          1: 'lime', 2: 'yellowgreen', 3: 'gold', 4: 'orange', 5: 'red',
          'неравенства': 'indigo'}


@app.route('/', methods=['GET'])
def main():
    return render_template('home.html', tags=possible_tags)


@app.route('/find_problems/', methods=['POST'])
def find_problems():
    if request.method == 'POST':
        lower_complexity = int(request.form['lower_complexity'])
        upper_complexity = int(request.form['upper_complexity'])
        required_tags = set()
        for key in request.form.keys():
            if key != 'lower_complexity' and key != 'upper_complexity':
                required_tags.add(key)
        global suitable_problems
        suitable_problems = set()
        global problems
        for problem in problems:
            if upper_complexity >= problem.complexity >= lower_complexity and \
                    len(required_tags.intersection(problem.tags)):
                suitable_problems.add(problem)
        return redirect('/problems/')


@app.route('/problems/', methods=['GET'])
def show_problems():
    global suitable_problems
    global colors
    return render_template('problems.html', problems=suitable_problems, colors=colors)


@app.route('/generate_olympiad/', methods=['POST'])
def gen_olymp():
    global problems
    global suitable_problems
    suitable_problems = generate_olympiad(problems)
    return redirect('/olympiad/')


@app.route('/olympiad/')
def get_olympiad():
    global suitable_problems
    return render_template('olympiad.html', problems=suitable_problems)


if __name__ == '__main__':
    app.run(debug=True)

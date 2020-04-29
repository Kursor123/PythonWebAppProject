from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class Problem:
    def __init__(self, complexity, tags, text):
        self.complexity = complexity
        self.tags = tags
        self.text = text


suitable_problems = set()


def load_problems(filename):
    problems = set()
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
                problems.add(Problem(complexity, tags, text))
            i += 1
    return (problems, possible_tags)


problems, possible_tags = load_problems('problems.txt')

colors = {'алгебра': 'orchid', 'геометрия': 'skyblue',
          'комбинаторика': 'lightgreen', 'теория чисел': 'crimson',
          'игры': 'cyan', 'чётность': 'darkkhaki', 'алгоритмы': 'navy',
          1: 'lime', 2: 'yellowgreen', 3: 'gold', 4: 'orange', 5: 'red'}


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


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

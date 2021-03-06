from flask import Flask, render_template


version = '1.0.1'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', version=version)

@app.route('/app')
def main():
    return render_template('app.html', version=version)

@app.route('/app/base64')
def b64():
    return render_template('b64.html', version=version)

@app.route('/help')
def help():
    return render_template('help.html', version=version)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=80)

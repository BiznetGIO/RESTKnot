from flask import Flask, render_template, session, request
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, 
            host=os.getenv('APP_HOST', 'localhost'),
            port=6968)

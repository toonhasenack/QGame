from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        # Perform any desired operations with the input data
        # Return a response or update variables as needed
        
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        # Process user input
        name = request.form['name']

    return render_template('game.html')

if __name__ == '__main__':
    app.run()
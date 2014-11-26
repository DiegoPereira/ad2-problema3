from flask import Flask
app = Flask(__name__)

@app.route('/cade_o_leite_que_tava_aqui', methods=['GET'])
def hello():
    return "O gato 'comeu'!"

if __name__ == "__main__":
    app.run()

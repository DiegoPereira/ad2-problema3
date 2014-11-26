import json

from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/hello')
def get_db():
    #user_id = request.args.get('user_id') aqui eh pra pegar argumento da url viss tales
    resp = make_response() #aqui faz uma resposta chamando uma funcao dentro do make_response
    resp.headers['Access-Control-Allow-Origin'] = "*" #sempre deixa isso
    return 'abc'
    #return resp


if __name__ == '__main__':
    app.debug = True    
    app.run(host='0.0.0.0', port=9090)
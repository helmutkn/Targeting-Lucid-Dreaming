from flask import Flask, request

app = Flask(__name__)

@app.route('/webhookcallback/sleepstate', methods=['POST'])
def sleepStateHook():
    state = request.values.get('state')
    epoch = request.values.get('epoch')

    print(f'state: {state}')
    print('epoch: ' + str(epoch))

    return "received"

@app.route('/webhookcallback/hello', methods=['POST'])
def helloHook():
    msg = request.values.get('hello')
    print(f'hello message sent. message: {msg}')

    return "received"


if __name__ == '__main__':
    app.run()

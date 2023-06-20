import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from api import qa_robot
from api.utils import init_logger

app = Flask(__name__)
CORS(app)


@app.route('/api/kbqa', methods=["POST"])
def predict():
    data = request.get_data('data')
    data = json.loads(data)
    query = data['query']
    
    if query == "":
        reply = "输入的内容不得为空，请您重新输入！"
    elif query.isdigit():
        reply = "输入的内容有误，请您重新输入！"
    else:
        reply = qa_robot(query).get("replay_answer")

    return jsonify({"reply": reply})


if __name__ == '__main__':
    init_logger()
    app.run(debug=True)

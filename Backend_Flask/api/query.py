from py2neo import Graph

from api.predict import predict
from api.template import templates

graph = Graph("127.0.0.1:7474",
              user="neo4j",
              password="15421312z")
model_dir = "api/model/osqa_model"
reply_output_file = "query_reply_output.txt"


def neo4j_searcher(cql):
    ress = ""
    data = graph.run(cql).data()
    if not data:
        return ress
    rst = []
    for d in data:
        d = list(d.values())
        if isinstance(d[0], list):
            rst.extend(d[0])
        else:
            rst.extend(d)

    data = "、".join([str(i) for i in rst])
    ress += data

    return ress


def write_file(reply, reply_output_file):
    with open(reply_output_file, "w", encoding="utf-8") as f:
        f.write(reply)


def semantic_parser(query):
    query_pred = predict(model_dir, query)

    if query_pred.intent_label in ["Definition", "Constitution", "Function", "Classification"]:
        qa_data = templates.get(query_pred.intent_label)
        qa_data["slot_value"] = query_pred.slot_words
        qa_data["slot_label_value"] = query_pred.slot_label
    else:
        qa_data = templates.get("Error")

    return qa_data


def get_answer(data):
    cql_template = data.get("cql_template")
    reply_template = data.get("reply_template")
    slot_value = data.get("slot_value")
    slot_label_value = data.get("slot_label_value")

    cql = cql_template.format(Label=slot_label_value, Entity=slot_value)
    answer = neo4j_searcher(cql)
    if not answer:
        data["replay_answer"] = "唔~我装满知识的大脑此刻很贫瘠。"
    else:
        pattern = reply_template.format(Entity=slot_value)
        data["replay_answer"] = pattern + answer

    return data


def qa_robot(query):
    qa_data = semantic_parser(query)

    if qa_data["intent_label"] == "Error":
        qa_data["replay_answer"] = "输入的内容有误，请您重新输入！"
    elif qa_data["slot_value"] == "":
        qa_data["replay_answer"] = "输入的内容有误，请您重新输入！"
    else:
        qa_data = get_answer(qa_data)
    return qa_data

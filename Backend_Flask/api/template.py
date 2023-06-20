templates = {
    "Background": {},
    "Definition": {
        "intent_label": "Definition",
        "slot_value": None,
        "slot_label_value": None,
        "slot_list": ["Entity"],
        "slot_label": ["Label"],
        "cql_template": "MATCH(p:{Label}) WHERE p.name='{Entity}' RETURN p.info",
        "reply_template": "{Entity}的定义如下：\n"
    },
    "Constitution": {
        "intent_label": "Constitution",
        "slot_value": None,
        "slot_label_value": None,
        "slot_list": ["Entity"],
        "slot_label": ["Label"],
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}的构成如下：\n"
    },
    "Feature": {},
    "Function": {
        "intent_label": "Function",
        "slot_value": None,
        "slot_label_value": None,
        "slot_list": ["Entity"],
        "slot_label": ["Label"],
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}的功能如下：\n"
    },
    "Classification": {
        "intent_label": "Classification",
        "slot_value": None,
        "slot_label_value": None,
        "slot_list": ["Entity"],
        "slot_label": ["Label"],
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}包含如下类型：\n"
    },
    "Effect": {},
    "Method": {},
    "Relationship": {},
    "Evaluation": {},
    "Error":{
        "intent_label": "Error",
    }
}

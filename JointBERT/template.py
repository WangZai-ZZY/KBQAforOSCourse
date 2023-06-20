templates = {
    "Background": {},
    "Definition": {
        "slot_list": ["Entity"],
        "slot_value": None,
        "slot_label": ["Label"],
        "slot_label_value": None,
        "cql_template": "MATCH(p:{Label}) WHERE p.name='{Entity}' RETURN p.info",
        "reply_template": "{Entity}的定义如下：\n"
    },
    "Constitution": {
        "slot_list": ["Entity"],
        "slot_value": None,
        "slot_label": ["Label"],
        "slot_label_value": None,
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}的构成如下：\n"
    },
    "Feature": {},
    "Function": {
        "slot_list": ["Entity"],
        "slot_value": None,
        "slot_label": ["Label"],
        "slot_label_value": None,
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}的功能如下：\n"
    },
    "Classification": {
        "slot_list": ["Entity"],
        "slot_value": None,
        "slot_label": ["Label"],
        "slot_label_value": None,
        "cql_template": "MATCH(p:{Label})-[r:CONTAIN]->(q) WHERE p.name='{Entity}' RETURN q.name",
        "reply_template": "{Entity}包含如下类型：\n"
    },
    "Effect": {},
    "Method": {},
    "Relationship": {},
    "Evaluation": {},
}

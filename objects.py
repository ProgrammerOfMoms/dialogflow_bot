import json

FACULTY_GET_FACULTY_POSTFIX = '''Вот список факультетов:
Факультет автоматики и вычислительной техники (АВТФ)
Факультет летательных аппаратов (ФЛА)
Механико-технологический факультет (МТФ)
Факультет мехатроники и автоматизации (ФМА)
Факультет пpикладной математики и информатики (ФПМИ)
Факультет радиотехники и электроники (РЭФ)
Физико-технический факультет (ФТФ)
Факультет энергетики (ФЭН)
Факультет бизнеса (ФБ)
Факультет гуманитарного образования (ФГО)
Институт социальных технологий (ИСТ)'''

POSTFIX = {
    "faculty.get": {
        "faculty": FACULTY_GET_FACULTY_POSTFIX
        }
}

PREFIX = {}

DEFAULT_KEYBOARD = {
    "one_time": False,
    "buttons": []
}

DIRECTION_BY_SUBJECTS_KEYBOARD = {
    "one_time": False,
    "buttons": [
    [
     {
        "action": {
            "type": "text",
            "label": "Еще",
            "payload": json.dumps({"command":"direction.by_subjects.more"})
        },
        "color": "default"
     }
    ],
    [
     {
        "action": {
            "type": "text",
            "label": "Отмена",
            "payload": json.dumps({"command":"direction.cancel"})
        },
        "color": "default"
     }
    ]
 ]
}

DIRECTION_BY_SPHERES_KEYBOARD = {
    "one_time": False,
    "buttons": [
    [
     {
        "action": {
            "type": "text",
            "label": "Еще",
            "payload": json.dumps({"command":"direction.by_spheres.more"})
        },
        "color": "default"
     }
    ],
    [
     {
        "action": {
            "type": "text",
            "label": "Отмена",
            "payload": json.dumps({"command":"direction.cancel"})
        },
        "color": "default"
     }
    ]
 ]
}

FEEDBACK_KEYBOARD = {
    "one_time": False,
    "inline": True,
    "buttons": [
    [
     {
        "action": {
            "type": "text",
            "label": "Да",
            "payload": json.dumps({"command":"feedback.positive"})
        },
        "color": "positive"
     },
     {
        "action": {
            "type": "text",
            "label": "Нет",
            "payload": json.dumps({"command":"feedback.negative"})
        },
        "color": "negative"
     }
    ]
 ]
}

KEYBOARDS = {
    "default": DEFAULT_KEYBOARD,
    "direction_by_subjects": DIRECTION_BY_SUBJECTS_KEYBOARD,
    "direction_by_spheres": DIRECTION_BY_SPHERES_KEYBOARD,
    "feedback": FEEDBACK_KEYBOARD
}
import logging
from modules.db import mysql_tools
from configs import action_code
from modules.Senswords import SensWord


def add_sensitive_word(word):
    session = mysql_tools.Session()

    new_data = SensWord(sensitive_word=word)

    session.add(new_data)
    session.commit()

    return new_data


def find_sensitive_word(word):
    session = mysql_tools.Session()
    query = session.query(SensWord).filter(SensWord.sensitive_word.like(f'%{word}%'))

    total_count = query.count()

    data_all = query.all()

    for adpos in data_all:
        adpos_data = {
            'id': adpos.id,
            'name': adpos.name
        }
        adpos_data_collection.append(adpos_data)

    return {"total_count": total_count, 'info': adpos_data_collection}


def remove(word):
    session = mysql_tools.Session()

    word_to_delete = session.query(SensWord).filter(SensWord.sensitive_word == word).first()

    if word_to_delete:
        session.delete(word_to_delete)
        session.commit()
    return


def load(page_index, page_limit):
    page_offset = (page_index - 1) * page_limit

    session = mysql_tools.Session()

    query = session.query(SensWord)

    total_count = query.count()

    query = query.limit(page_limit)
    query = query.offset(page_offset)

    data_all = query.all()

    results = []

    for sensword in data_all:
        sensword_data = {
            'id': sensword.id,
            'sens_word': sensword.sensitive_word,
            'updated_at': sensword.updated_at
        }
        results.append(sensword_data)

    return {"total_count": total_count, "info": results}


def load_all():
    session = mysql_tools.Session()

    query = session.query(SensWord)

    total_count = query.count()

    data_all = query.all()

    results = []

    for sensword in data_all:
        sensword_data = {
            'id': sensword.id,
            'sens_word': sensword.sensitive_word,
            'updated_at': sensword.updated_at
        }
        results.append(sensword_data)

    return {"total_count": total_count, "info": results}

""" An interface for the words stored in the database. """
import sqlite3

def unwrap_result(t):
    if t is None:
        return None
    return t[0]

def get_id_for_word(cursor, word):
    """ Get the id of a word, given the word. """
    query = 'select word_id from words where word = ?'
    result = cursor.execute(query, (word,))
    return unwrap_result(result.fetchone())

def get_word_for_id(cursor, word_id):
    """ Get word for given id. """
    query = "select word from words where word_id = ?"
    result = cursor.execute(query, (word_id,))
    return unwrap_result(result.fetchone())

def word_exists(cursor, word):
    """ Returns true if words is in database. """
    return get_id_for_word(word) is not None

def get_word_list(cursor):
    """ Return a list of all words. """
    query = "select word from words"
    result = cursor.execute(query)
    return [unwrap_result(r) for r in result.fetchall()]

def append_word(cursor, word):
    """ Append a word to the database. """
    query = "INSERT INTO words (word) VALUES (?)"
    cursor.execute(query, (word,))

""" An interface for the words stored in the database. """
import sqlite3


def get_id_for_word(cursor, word):
    """ Get the id of a word, given the word. """
    query = 'select word_id from words where word = ?'
    result = cursor.execute(query, (word,))
    return result.fetchone()


def get_word_for_id(cursor, word_id):
    """ Get word for given id. """
    query = "select word from words where word_id = ?"
    result = cursor.execute(query, (word_id,))
    return result.fetchone()


def word_exists(cursor, word):
    """ Returns true if words is in database. """
    return get_id_for_word(cursor, word) is not None


def get_word_list(cursor, ids=False):
    """ Return a list of all words. """
    query = "select word, soundex from words"
    if ids is True:
        query = "select word, word_id, soundex from words"
    result = cursor.execute(query)
    return {word[0]: word[1:] for word in result.fetchall()}


def append_word(cursor, word):
    """ Append a word to the database. """
    query = "INSERT INTO words (word) VALUES (?)"
    cursor.execute(query, (word,))

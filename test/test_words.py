from db import words


def test_get_id_for_word(db_conn):
    cursor = db_conn.cursor()
    assert words.get_id_for_word(cursor, '&c') == (1,)
    # Should also test when the word *doesn't* exist in the database
    assert words.get_id_for_word(cursor, 'rgnthm') is None


def test_get_word_for_id(db_conn):
    cursor = db_conn.cursor()
    # Test the affirmative case
    assert words.get_word_for_id(cursor, 35810) == ('boogaloo',)
    # Let's test on a few that obviously aren't valid ids
    assert words.get_word_for_id(cursor, -1) is None
    assert words.get_word_for_id(cursor, 1.5) is None
    assert words.get_word_for_id(cursor, 'wjksjksjkadbf') is None


def test_word_exists(db_conn):
    cursor = db_conn.cursor()

    assert words.word_exists(cursor, 'boogaloo')
    assert words.word_exists(cursor, '&c')
    assert not words.word_exists(cursor, 'rgnthm')
    assert not words.word_exists(cursor, 4)


def test_get_word_list(db_conn):
    cursor = db_conn.cursor()
    dct = words.get_word_list(cursor)
    assert len(dct) == 354971
    assert 'boogaloo' in dct
    assert 'rgnthm' not in dct
    dct = words.get_word_list(cursor, ids=True)
    assert all(len(value) == 2 for value in dct.values())


def test_append_word(db_conn):
    cursor = db_conn.cursor()
    words.append_word(cursor, 'rgnthm')
    assert words.word_exists(cursor, 'rgnthm')

import collections
from pyphonetics import RefinedSoundex
from Levenshtein import distance
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from ui import speller
from engine import classifier, frequency, utilities
from db import words
import sqlite3
import sys
import re

DATABASE_LOCATION = 'db/data.db'
CLASSIFIER_REVISION = 1
NUMBER_RE = re.compile('[0-9]+')

# Word describes a given correction, what the word is, where it starts and where it ends.
Word = collections.namedtuple('Word', ['value', 'start', 'end'])


def properties_of(word, word_soundex, candidate, candidate_soundex):
    ''' Map a word to a list of True/False points that describe it's properties  '''
    sounds_similar = 'sounds_similar' if word_soundex == candidate_soundex else 'sounds_dissimilar'
    # similarity in terms of edit distance is defined as < 3
    similar = 'similar' if distance(word, candidate) < 3 else 'dissimilar'
    start_same = 'starts_same' if word[0] == candidate[0] else 'different_start'
    return [sounds_similar, similar, start_same]


def correct_words_according_to(word_tuple, word_classifier, dictionary):
    ''' Take a given word, and feed it into the classifier, returning a list of
    words that are likely correct. '''
    word = word_tuple.value
    soundex = RefinedSoundex()
    word_soundex = soundex.phonetics(word)
    corrections = []
    # for every word in the dictionary
    for candidate, metadata in dictionary.items():
        # get the properties of the dictionary word and run that through the
        # classifier
        index, candidate_soundex = metadata
        properties = properties_of(word,
                                   word_soundex,
                                   candidate,
                                   candidate_soundex)
        # Compute the rank of the word based on how frequently it is used in
        # the English language.
        word_rank = frequency.frequency_of(index)
        assumptions = {
            'correct': 1 - word_rank,
            'incorrect': word_rank
        }
        probability, cls = word_classifier.classify(properties,
                                                    assumptions=assumptions)
        if cls == 'correct':
            corrections.append((probability, candidate))
    return word_tuple, sorted(corrections, reverse=True)


class Correcter:
    def __init__(self, dictionary, classifier, words):
        ''' Initialize Corrector class. '''
        self.correcting_words = utilities.CyclicList(values=words)
        self.cached_corrections = {}
        self.classifier = classifier
        self.dictionary = dictionary
        self.cur_node = None

    def update(self, words):
        ''' Update the list of unrecognized words. '''
        self.correcting_words = utilities.CyclicList(values=words)
        self.cur_node = None

    def next(self):
        ''' Return corrections for the next unrecognized word. '''
        # If the current_node is None, initialize it at the head of the list
        if self.cur_node is None:
            self.cur_node = self.correcting_words.head
        else:
            self.cur_node = self.cur_node.next_node

        word_to_correct = self.cur_node.value

        # Check if the word hasn't been corrected before
        if word_to_correct.value not in self.cached_corrections:
            correction_data = correct_words_according_to(word_to_correct, self.classifier, self.dictionary)
            self.cached_corrections[word_to_correct.value] = correction_data

        # update the cache with new word.
        self.cached_corrections[word_to_correct.value] = (word_to_correct,
                                                          *self.cached_corrections[word_to_correct.value][1:])

        return self.cached_corrections[word_to_correct.value]

    def prev(self):
        ''' Return corrections for the previous unrecognized word. '''
        # If the current_node is None, initialize at the tail of the list.
        # Initializing the current node at the end of the list gives the
        # impression of the user starting from the end of the available
        # corrections rather than the start
        if self.cur_node is None:
            self.cur_node = self.correcting_words.tail
        else:
            self.cur_node = self.cur_node.prev_node

        word_to_correct = self.cur_node.value

        # Check if the word hasn't been corrected before
        if word_to_correct.value not in self.cached_corrections:
            correction_data = correct_words_according_to(word_to_correct, self.classifier, self.dictionary)
            self.cached_corrections[word_to_correct.value] = correction_data

        # update the cache with new word.
        self.cached_corrections[word_to_correct.value] = (word_to_correct,
                                                          *self.cached_corrections[word_to_correct.value][1:])
        return self.cached_corrections[word_to_correct.value]

    @property
    def empty(self):
        ''' Returns True if there are no words to correct. '''
        return self.correcting_words.length == 0


class UIManager:
    ''' Manage UI state. '''
    def get_editor_words(self):
        '''return a list of the words in the text (just a simple text string
        split by a space).'''

        text_editor_text = self.main_window_state.textEdit.toPlainText()
        return text_editor_text.split(' ')

    def get_unrecognized_words(self, candidates):
        text_editor_words = self.get_editor_words()
        cur_pos = 0
        unrecognized_words = []

        # go through every word in the text editor
        for word in text_editor_words:
            lookup_word = word.strip('\'",.')
            # Sometimes the word is empty, ignore it if it is
            if word == '':
                continue
            # Else if it isn't a number and it isn't in the dictionary
            # Add it (along with where it starts and ends in the text) to the
            # list of unrecognized words.
            elif not NUMBER_RE.match(word) and lookup_word not in self.dictionary:
                word_tuple = Word(lookup_word, cur_pos, cur_pos + len(lookup_word))
                unrecognized_words.append(word_tuple)
            # move the current position forward by the length of the word and
            # the space separating it from the next word.
            cur_pos += len(word) + 1
        return unrecognized_words

    def get_words(self):
        ''' Retrieve a list of words from the words database. '''
        cursor = self.conn.cursor()
        return words.get_word_list(cursor, ids=True)

    def replace_word(self, word, item_index):
        text_editor = self.main_window_state.textEdit
        text_editor_text = text_editor.toPlainText()
        item = self.corrections_model.itemFromIndex(item_index)
        # Plus side to immutable strings: Immutable strings
        # Down side to immutable strings: You have to copy the string any time
        # you mutate it.
        text_editor_text = text_editor_text[:word.start] + item.text() + text_editor_text[word.end:]
        text_editor.setText(text_editor_text)

    def get_text_cursor(self):
        ''' Return the current cursor position inside the text editor. '''
        return self.main_window_state.textEdit.textCursor()

    def display_corrections(self, word, corrections):
        ''' Display a word with it's corrections in the spelling sidebar. '''
        list_view = self.main_window_state.corrections_view

        model = self.corrections_model
        cursor = self.get_text_cursor()
        # Move the cursor to highlight the current word we're looking at.
        cursor.setPosition(word.start)
        cursor.setPosition(word.end, QtGui.QTextCursor.KeepAnchor)
        self.main_window_state.textEdit.setTextCursor(cursor)
        # Let the user know which word we're correcting.
        self.main_window_state.correction_label.setText(word.value)
        model.clear()
        # For some reason disconnecting a qt action causes it to pack a hissy fit.
        try:
            list_view.activated.disconnect()
        except Exception:
            pass
        list_view.activated.connect(lambda item: self.replace_word(word, item))
        # take up to 10 corrections from the classifier's output
        end = min(10, len(corrections))
        for _, correction in corrections[:end]:
            item = QStandardItem()
            item.setText(correction)
            model.appendRow(item)

    def next_word(self):
        ''' Take the next unrecognized word and display it. '''
        if self.correcter.empty is False:
            correction = self.correcter.next()
            self.display_corrections(*correction)

    def prev_word(self):
        ''' Take the previous unrecognized word and display it. '''
        if self.correcter.empty is False:
            correction = self.correcter.prev()
            self.display_corrections(*correction)

    def update_mistakes(self):
        ''' Scan the document for new errors. '''
        unrecognized_words = self.get_unrecognized_words(self.get_editor_words())
        self.corrections_model.clear()
        self.main_window_state.correction_label.setText("Correction")
        self.correcter.update(unrecognized_words)

    def connect_slots(self):
        ''' Connect UI slots for various ui objects. '''
        self.main_window_state.next_word.pressed.connect(self.next_word)
        self.main_window_state.previous_word.pressed.connect(self.prev_word)
        self.main_window_state.textEdit.textChanged.connect(self.update_mistakes)

    def load_classifier(self):
        ''' Load the classifier from the database. '''
        cursor = self.conn.cursor()
        db_classifier = classifier.Classifier()
        classifier_query = f'SELECT classifier.classifier_data FROM classifier WHERE classifier.classifier_id = {CLASSIFIER_REVISION}'
        result = cursor.execute(classifier_query)
        db_classifier.deserialize_from(result.fetchone())
        self.classifier = db_classifier

    def __init__(self):
        ''' Setup UI objects. '''
        self.application = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window_state = speller.Ui_MainWindow()
        self.main_window_state.setupUi(self.main_window)
        self.connect_slots()

    def run(self):
        ''' Run UIManager. '''
        with sqlite3.connect(DATABASE_LOCATION) as conn:
            self.conn = conn
            self.load_classifier()
            self.dictionary = self.get_words()
            self.correcter = Correcter(self.dictionary, self.classifier, [])
            self.corrections_model = QStandardItemModel()
            self.main_window_state.corrections_view.setModel(self.corrections_model)
            self.main_window.show()
            res = self.application.exec_()
        return res

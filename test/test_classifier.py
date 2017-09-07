from engine import classifier
from enum import Enum
import collections


class Class(Enum):
    ''' Dummy Enum representing classes. '''
    BANANA = 0
    APPLE = 1
    ORANGE = 2


# Maps properties of each class to classes, e.g long, yellow, sweet -> banana.
TEST_DATASET = {
    Class.BANANA: [["long", "yellow", "sweet"],
                    ["long", "bruised", "yellow", "sweet"],
                    ["long", "yellow", "sweet"],
                    ["long", "bruised", "yellow", "ripe"],
                    ["yellow", "sweet", "rotten"]],
    Class.APPLE: [["round", "bruised", "red"],
                  ["round", "red", "sweet", "juicy"],
                  ["rotten", "round", "green", "sweet"],
                  ["round", "green", "sour"]],
    Class.ORANGE: [["round", "orange", "juicy", "sour"],
                   ["round", "ripe", "orange"],
                   ["round", "orange", "sweet"],
                   ["round", "orange", "sour"]]
}
# Size: 13
# P(B) = 5/13
# P(A) = 4/13
# P(O) = 4/13


def test_group_class():
    test_arr = [
        [1, "green", "blue"],
        [1, "red", "yellow"],
        [2, "orange", "blue"]
    ]

    # Making sure the mapping function works correctly, assigning the class id
    # (taken by default as the first value of the list) to be a key of a
    # dictionary grouping by class.
    assert classifier.group_by_class(test_arr) == {
        1: [["green", "blue"], ["red", "yellow"]],
        2: [["orange", "blue"]]
    }


def test_classifier():
    bclassifier = classifier.Classifier()
    bclassifier.train(TEST_DATASET)

    # Basically testing that the classifier returns what it should return with
    # the given input.

    # orange is a trait exclusive to oranges so the identified class should be
    # orange.
    _, prediction = bclassifier.classify(["round", "sour", "orange"])
    assert prediction == Class.ORANGE

    # Whilst there are bruised apples, and sweet oranges, only banana has both
    # and therefore should be the identified class.
    _, prediction = bclassifier.classify(["bruised", "sweet"])
    assert prediction == Class.BANANA

    # The ripe trait occurs once in both bananas and oranges, but bananas are
    # most likely /overall/ and therefore the identified class should be
    # banana.
    _, prediction = bclassifier.classify(["ripe"])
    assert prediction == Class.BANANA

    # Both apples and oranges have the round and the sour trait, but because
    # oranges exhibit this trait more often the returned class should be
    # orange.
    _, prediction = bclassifier.classify(["round", "sour"])
    assert prediction == Class.ORANGE

    # Ditto for this case, apples and oranges have round and sweet, but apples
    # more often therefore the class should be apple.
    _, prediction = bclassifier.classify(["round", "sweet"])
    assert prediction == Class.APPLE

    # This shouldn't realistically happen, but I do test if the classifer is passed things
    # that aren't in any of the three classes sets. In this case it should return (0, None).
    prediction = bclassifier.classify(['pink'])
    assert prediction == (0, None)


def test_classifier_json():
    bclassifier = classifier.Classifier()
    result_type = classifier.Type('class', 1)
    result_type.train([[1, 2, 3]])
    bclassifier.classes.append(result_type)
    assert bclassifier.as_json() == {'__classifier__': True,
                                     'classes': [result_type]}


def test_type():
    btype = classifier.Type('class', 1)
    assert btype.summarize() == (1, collections.Counter())
    assert repr(btype) == f'Type(class, {collections.Counter()})'
    assert btype.as_json() == {'__type__': True,
                               'class': 'class',
                               'class_probability': 1,
                               'properties': collections.Counter()}

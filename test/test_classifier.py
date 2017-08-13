from engine import classifier
from enum import Enum


class Class(Enum):
    BANNANA = 0
    APPLE = 1
    ORANGE = 2


TEST_DATASET = {
    Class.BANNANA: [["long", "yellow", "sweet"],
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
    assert classifier.group_by_class(test_arr) == {
        1: [["green", "blue"], ["red", "yellow"]],
        2: [["orange", "blue"]]
    }


def test_classifier():
    bclassifier = classifier.Classifier()
    bclassifier.train(TEST_DATASET)
    _, prediction = bclassifier.classify(["round", "sour", "orange"])
    assert prediction == Class.ORANGE
    _, prediction = bclassifier.classify(["bruised", "sweet"])
    assert prediction == Class.BANNANA
    _, prediction = bclassifier.classify(["ripe"])
    assert prediction == Class.BANNANA
    _, prediction = bclassifier.classify(["round", "sour"])
    assert prediction == Class.ORANGE
    _, prediction = bclassifier.classify(["round", "sweet"])
    assert prediction == Class.APPLE

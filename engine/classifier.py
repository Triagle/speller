""" A naive bayesian classifier implementation that provides a general purpose,
yet flexible method of classifying objects into classes. """

from db import Serializable
import json


class Type(Serializable):
    """ Calculates the probability that an object belongs to a given class. """

    def __init__(self, cls, class_probability):
        self.cls = cls
        self.class_probability = class_probability
        self.property_probability = {}

    def train(self, dataset):
        """ Train the type classifier from a dataset. """
        data_size = len(dataset)
        for point in dataset:
            for prop in point:
                if prop in self.property_probability:
                    self.property_probability[prop] += 1
                else:
                    self.property_probability[prop] = 1
        for prop, prob in self.property_probability.items():
            self.property_probability[prop] /= data_size

    def as_json(self):
        ''' Return a json friendly representation of Type class. '''
        return {'__type__': True,
                'class_probability': self.class_probability,
                'properties': self.property_probability}

    def summarize(self):
        """ Return probabilities of both classes and properties. """
        return (self.class_probability, self.property_probability)

    def probability(self, properties):
        """ Return the classification of an object given it's properties. """
        probability = self.class_probability
        for prop in properties:
            if prop in self.property_probability:
                probability *= self.property_probability[prop]
            else:
                return 0
        return probability


class Classifier(Serializable):
    """ General purpose bayesian classifier. """

    def __init__(self, classes=[]):
        ''' Initialize Classifier. '''
        self.classes = []
        serialize_table = {
            'data': 'json_rep'
        }
        super().__init__(serialize_table)

    def train(self, dataset):
        """ Train the classifier from a dataset. """
        dataset_length = sum([len(v) for _, v in dataset])
        for cls, points in dataset:
            cls_type = Type(cls, len(points) / dataset_length)
            cls_type.train(points)
            self.classes.append(cls_type)

    @property
    def json_rep(self):
        return json.dumps(self, cls=ClassifierEncoder)

    def as_json(self):
        ''' Return a json friendly representation of Classifier'''
        return {'__classifier__': True, 'classes': self.classes}

    def classify(self, properties):
        """ Classify an object into a class. """
        likely_cls = (None, 0)
        for cls in self.classes:
            prob = cls.probability(properties)
            (_, max_prob) = likely_cls
            if prob > max_prob:
                likely_cls = (cls.cls, prob)
        return likely_cls


class ClassifierEncoder(json.JSONEncoder):
    ''' Encode Classifier and Properties to json format for database
    insertion. '''
    def default(self, obj):
        if isinstance(obj, Classifier) or isinstance(obj, Type):
            return obj.as_json()


def group_by_class(dataset, cls_func=lambda x: (x[0], x[1:])):
    """ Group a list by it's class (or rather by function). e.g
    group_by_class(lambda x: (x[0], x[1:]), [[1, 2, 3], [1, 3, 4]])
    -> {1: [[2, 3], [3, 4]]} """
    classes = {}
    for point in dataset:
        cls, props = cls_func(point)
        if cls in classes:
            classes[cls].append(props)
        else:
            classes[cls] = [props]
    return classes

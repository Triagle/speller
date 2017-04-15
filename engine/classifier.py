""" A naive bayesian classifier implementation that provides a general purpose,
yet flexible method of classifying objects into classes. """
class Type:
    """ Calculates the probability that an object belongs to a given class. """
    cls = None
    property_probability = {}
    class_probability = 0

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

class Classifier:
    """ General purpose bayesian classifier. """
    classes = []
    def train(self, dataset):
        """ Train the classifier from a dataset. """
        dataset_length = sum([len(v) for _, v in dataset])
        for cls, points in dataset:
            cls_type = Type(cls, len(points) / dataset_length)
            cls_type.train(points)
            self.classes.append(cls_type)
    def classify(self, properties):
        """ Classify an object into a class. """
        likely_cls = (None, 0)
        for cls in self.classes:
            prob = cls.probability(properties)
            (_, max_prob) = likely_cls
            if prob > max_prob:
                likely_cls = (cls.cls, prob)
        return likely_cls

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

""" Calculate the probability of encountering a word w, given that it is within
the top 1000 most common words. P(r) is given by 0.1/r, where 1 < r < 1000.
1000 words is the limit as beyond that the harmonic series diverges for less
frequent words. About 50% of all words in the Oxford English Corpus reside in
the top 100 words. """


class Frequency():
    """ Contains the state for the frequency analysis. """
    frequency_map = None

    def __init__(self, frequency_map):
        self.frequency_map = frequency_map

    def rank(self, word):
        """ Rank a word according to zipf's law.
        e.g frequency.rank("the") -> 0.1 # (0.1 / 1)
        """
        if word not in self.frequency_map:
            return None
        return 0.1 / (self.frequency_map[word])


def frequency_from(wordlist):
    """ Return a frequency object from wordlist, a list of words ranked in
    order according to their commonality. """
    fmap = {}
    for index, value in enumerate(wordlist):
        fmap[value] = index + 1
    return Frequency(fmap)

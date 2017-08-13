""" Calculate the probability of encountering a word w, given that it is within
the top 1000 most common words. P(r) is given by 0.1/r, where 1 < r < 1000.
1000 words is the limit as beyond that the harmonic series diverges for less
frequent words. About 50% of all words in the Oxford English Corpus reside in
the top 100 words. """

HARMONIC_LIMIT = 1000


def frequency_of(rank, harmonic_limit=HARMONIC_LIMIT):
    """ Rank a word according to zipf's law.
    e.g frequency.rank("the") -> 0.1 # (0.1 / 1)
    """
    return 0.1 / min(rank, 10000)

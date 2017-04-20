class Learner:
    corrections = {}

    def __init__(self, corrections):
        self.corrections = corrections

    def has_misspelt(self, word, misspelling):
        if word not in self.corrections:
            return False
        return misspelling in self.corrections[word]

    def add_spellings(self, word, misspelling):
        if word not in self.corrections:
            self.corrections[word] = set()
        self.corrections[word] |= misspelling

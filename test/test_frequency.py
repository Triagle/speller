from engine import frequency

FLIST = [
    'a',
    'b',
    'c',
    'd'
]

def test_frequency_builder():
    frqncy = frequency.frequency_from(FLIST)
    assert frqncy.rank('a') == 0.1
    assert frqncy.rank('b') == 0.05
    assert frqncy.rank('c') == (0.1 / 3)
    assert frqncy.rank('d') == (0.1 / 4)

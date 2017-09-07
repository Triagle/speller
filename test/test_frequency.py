from engine.frequency import frequency_of

def test_frequency():
    assert frequency_of(1) == 0.1
    assert frequency_of(3) == (0.1 / 3)

# Test the user informed corrections (learner) module
from engine import learner


USER_CORRECTIONS = {
    # An example user misspelling confusing double letters
    "millennium": {"millenium", "milenium", "milennium"}
}

def test_learner():
     lrnr = learner.Learner(USER_CORRECTIONS)
     assert lrnr.has_misspelt("millennium", "milenium") == True
     assert lrnr.has_misspelt("believe", "beleive") == False
     lrnr.add_spellings("believe", {"beleive"})
     assert lrnr.has_misspelt("believe", "beleive") == True

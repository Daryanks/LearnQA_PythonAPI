class TestPhase:
    def test_phase_check(self):
        phrase = input("Set a phrase: ")

        assert len(phrase)<15, "Phrase longer than 15 characters"
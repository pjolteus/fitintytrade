# oracle_ai_model/tests/test_predict.py

import unittest
from predict_from_model import run_prediction

class TestPrediction(unittest.TestCase):
    def test_valid_symbol(self):
        result = run_prediction("AAPL", "lstm")
        self.assertIn("prediction", result)
        self.assertIn("probability", result)

    def test_invalid_symbol(self):
        result = run_prediction("INVALID", "lstm")
        self.assertEqual(result["status"], "error")

    def test_invalid_model(self):
        result = run_prediction("AAPL", "unsupported_model")
        self.assertEqual(result["status"], "error")

if __name__ == "__main__":
    unittest.main()

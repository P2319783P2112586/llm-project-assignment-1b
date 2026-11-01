"""
Unit and integration tests for Gemma-2B-IT.
"""

import unittest

from src.model import load_model, get_response


class TestGemmaIntegration(unittest.TestCase):
    """
    Integration tests using the actual Gemma model.
    The model is loaded only once for this test class.
    """

    @classmethod
    def setUpClass(cls):
        print("\nInitializing Gemma for integration tests...")
        cls.model, cls.tokenizer = load_model()

    def test_factual_query(self):
        """Test whether the model answers a factual question."""

        prompt = "What is the capital of France? Answer briefly."

        response = get_response(
            prompt,
            self.model,
            self.tokenizer,
            max_length=50,
            temperature=0.0,
        )

        self.assertIn("paris", response.lower())

    def test_code_generation(self):
        """Test whether the model can generate a factorial function."""

        prompt = (
            "Write a Python function named factorial(n) "
            "using a for loop. Return the factorial of n. "
            "Show the Python code."
        )

        response = get_response(
            prompt,
            self.model,
            self.tokenizer,
            max_length=180,
            temperature=0.0,
        )

        response_lower = response.lower()

        self.assertIn("def", response_lower)
        self.assertIn("factorial", response_lower)

        self.assertTrue(
            "for" in response_lower or "range" in response_lower,
            "The generated code should contain a loop."
        )


class TestInputValidation(unittest.TestCase):
    """Test invalid inputs without loading the model."""

    def test_empty_prompt(self):
        """An empty prompt should raise ValueError."""

        with self.assertRaises(ValueError):
            get_response(
                "   ",
                None,
                None,
            )

    def test_invalid_max_length(self):
        """A non-positive maximum length should be rejected."""

        with self.assertRaises(ValueError):
            get_response(
                "Hello",
                None,
                None,
                max_length=0,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

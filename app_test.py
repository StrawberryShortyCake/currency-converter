from unittest import TestCase
from app import app
import os
os.environ["FLASK_DEBUG"] = "0"

app.config['TESTING'] = True


class ConverterAppTestCase(TestCase):
    """Test currency converter app"""

    def test_homepage(self):
        """Test the home page shows the conversion form"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("I am the currency converter home page", html)
            self.assertIn("conversion-form", html)

    def test_converter_happy_path(self):
        """Test the converter function produces the correct converted amount"""
        with app.test_client() as client:
            mock_form_data = {
                'from_currency': 'USD',
                'to_currency': 'USD',
                'amount': '100'
            }

            response = client.post(
                '/result',
                data=mock_form_data
            )

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("$100", html)

    def test_converter_case_sensitivity(self):
        """Test the converter produces the correct converted amount despite
            case differences"""
        with app.test_client() as client:

            mock_form_data = {
                'from_currency': 'usd',
                'to_currency': 'USD',
                'amount': '100'
            }

            response = client.post(
                '/result',
                data=mock_form_data
            )

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("$100", html)

    def test_converter_case_invalid_amount(self):
        """Test the converter produces the correct error when an invalid
            amount is entered"""
        with app.test_client() as client:

            mock_form_data = {
                'from_currency': 'USD',
                'to_currency': 'USD',
                'amount': 'not_an_amount'
            }

            response = client.post(
                '/result',
                data=mock_form_data
            )

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Please enter a valid amount", html)

    def test_converter_case_invalid_code(self):
        """Test the converter produces the correct error when an invalid
            code is entered"""
        with app.test_client() as client:

            mock_form_data = {
                'from_currency': 'USD',
                'to_currency': 'not_a_code',
                'amount': '100'
            }

            response = client.post(
                '/result',
                data=mock_form_data
            )

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Please enter a valid currency code", html)

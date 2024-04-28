from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
from flask import Flask, request, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "seeeeecreeeeet-secret"


@app.get('/')
def show_homepage():
    """Show form for currency conversion."""

    return render_template("base.jinja")


@app.post('/result')
def show_conversion_result():
    """Check if input is valid, and if so, display the result.
        If the input is invalid, raise a message for invalid amount
        or invalid current code
    """

    converting_from = request.form["from_currency"].upper()
    converting_to = request.form["to_currency"].upper()

    error_message = ""

    """NOTES FOR INSTRUCTOR:
        I couldn't differentiate the error code coming from forex-python,
        but validating before passing the input values over seemed to veer
        away from the lessons of the week. I chose to go with try...except
        to handle errors, but it might not be exactly what's required. In
        work setting, I would've set up a meeting with the PM to discuss
        requirements and constraints.
        I also THINK that all these code is relevant to the route, but
        it does concern me that I don't have another python file.
    """

    try:
        amount_to_convert = int(request.form["amount"])
    except ValueError as error_details:
        error_message = "Please enter a valid amount."
        print("ERROR DETAILS:", error_details)

        return render_template(
            "error.jinja",
            error_message=error_message
        )

    try:
        amount_converted = format(CurrencyRates().convert(
            converting_from, converting_to, amount_to_convert), ".2f")
    except RatesNotAvailableError as error_details:
        error_message = "Please enter a valid currency code."
        print("ERROR DETAILS:", error_details)

        return render_template(
            "error.jinja",
            error_message=error_message
        )

    converted_currency_sign = CurrencyCodes().get_symbol(converting_to)

    return render_template(
        "result.jinja",
        converted_currency_sign=converted_currency_sign,
        amount_converted=amount_converted)

# CloudBleed Checker for LastPass

This is a script that is designed to help check your LastPass database for sites that could have been leaked by the [CloudBleed](https://github.com/pirate/sites-using-cloudflare) bug.

# Usage

If you don't have `pip` (Python package manager) installed, you can install it with this command:

    curl https://bootstrap.pypa.io/get-pip.py | python

Install the dependencies using `pip`.

    pip install lastpass-python requests

Your `pip` directory may be set up in a way that requires sudo access. If that is the case, run this command:

    sudo pip install lastpass-python requests

Then, run the script.

    python cloudbleed_check.py


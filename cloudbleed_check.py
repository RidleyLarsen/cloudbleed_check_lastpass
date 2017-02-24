#!/usr/bin/env python
# coding: utf-8
import json
import os
import sys
import requests
from getpass import getpass
from urlparse import urlparse
from lastpass import (
    Vault,
    LastPassIncorrectYubikeyPasswordError,
    LastPassIncorrectGoogleAuthenticatorCodeError
)

SITE_LEAKS_URL = "https://github.com/pirate/sites-using-cloudflare/blob/master/sorted_unique_cf.txt?raw=true"

def main():
    username = raw_input("Enter your LastPass Username: ")
    password = getpass("Enter your LastPass Master Password (will not be shown): ")

    try:
        # First try without a multifactor password
        vault = Vault.open_remote(username, password)
    except LastPassIncorrectGoogleAuthenticatorCodeError as e:
        # Get the code
        multifactor_password = input('Enter Google Authenticator code:')

        # And now retry with the code
        vault = Vault.open_remote(username, password, multifactor_password)
    except LastPassIncorrectYubikeyPasswordError as e:
        # Get the code
        multifactor_password = input('Enter Yubikey password:')

        # And now retry with the code
        vault = Vault.open_remote(username, password, multifactor_password)

    accounts = {}
    for i, acc in enumerate(vault.accounts):
        uri = urlparse(acc.url)
        accounts[uri.netloc] = True

    with open("leaked_sites.txt", "wb") as f:
        print "Downloading leaked_sites.txt"
        response = requests.get(SITE_LEAKS_URL, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=total_length/100):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()
            sys.stdout.write("\n")

    compromised_sites = []
    with open("leaked_sites.txt", "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            try:
                site_name = line if accounts[line] else None
                if site_name not in compromised_sites:
                    compromised_sites.append(site_name)
                    print "{0} was compromised.".format(site_name)
            except KeyError:
                pass

if __name__ == "__main__":
    main()

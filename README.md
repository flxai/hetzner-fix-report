# Template for Python packages

This is a template repository for building Python packages. It allows you to quickstart
your Python package.

## Using it

- Click on [Use this template](https://github.com/soerface/template-python-package/generate)
- A workflow "Use template" will start automatically. It will rename "hello_gh_actions" to whatever you have chosen for your repository name
- After one or two minutes, a new commit will appear on your master branch. Checkout the diff to see if everything is alright!

To be able to publish documentation and package, follow these steps:

- Create an account on [readthedocs](https://readthedocs.org/) and connect this repository
- Create an account on [PyPI](https://pypi.org) and generate an API-Key for your project

Go to your repositories "Settings -> Secrets" page and add the `PYPI_API_KEY` secret with the key you received from PyPI.

Below is a README example. It will be used for your repository.

---

# Hello GitHub Actions

[![Documentation Status](https://readthedocs.org/projects/hello-gh-actions/badge/?version=latest)](https://hello-gh-actions.readthedocs.io/en/latest/?badge=latest)
[![Tests Status](https://github.com/soerface/template-python-package/workflows/CI/badge.svg)](https://github.com/soerface/template-python-package/actions?query=workflow%3ACI)

- Documentation: https://hello-gh-actions.readthedocs.io
- PyPI: https://pypi.org/project/hello-gh-actions

## Getting started

Installation via pip:

    pip install hello_gh_actions
    
Using the fizzbuzz:

    >>> from hello_gh_actions.fizzbuzz import fizzbuzz
    >>> fizzbuzz(35)
    'fizzbuzz'

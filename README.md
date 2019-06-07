## MagneticInteractionsChallenge

*[ TODO Add project description]*

## How to Run

First, make sure that you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) installed and install the project.

```shell
mkvirtualenv MagneticInteractionsChallenge
pip install -e 'git+https://github.com/cmpatino/MagneticInteractionsChallenge.git#egg=magnetic_interactions'
```

> For a private repository accessible only through an SSH authentication, substitute `git+https://github.com` with `git+ssh://git@github.com`.

*[ TODO Add instructions to run package scritps ]*

## How to Contribute

First, make sure that you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) installed and install the project in development mode.

```shell
mkvirtualenv MagneticInteractionsChallenge
git clone https://github.com/cmpatino/MagneticInteractionsChallenge.git
cd MagneticInteractionsChallenge
pip install -r requirements.txt
pip install -e .
pip freeze | grep -v magnetic_interactions > requirements.txt
```

> For a private repository accessible only through an SSH authentication, substitute `https://github.com/` with `git@github.com:`.

Then, create or select a GitHub branch and have fun... 
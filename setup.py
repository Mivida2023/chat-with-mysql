#lancer cette commande pour installer le package
# pip install -e .

from setuptools import setup, find_packages

setup(
    name='cwsql',
    version='0.1',
    packages=find_packages(where="src/cwsql"),
    package_dir={"": "src/cwsql"}
)

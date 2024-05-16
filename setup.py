from setuptools import setup, find_packages

setup(
    name='http_load_testing',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Kushagra Ghosh',
    author_email='kushagra.ghosh@duke.edu',
)
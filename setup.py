from setuptools import setup, find_packages

setup(
    name='tm',
    version='0.0.1dev1',
    description='An automated trading machine which finds itself a good trading strategy',
    author='Philipp Page, Jonathan Feldges, Nico Hakenes',
    author_email='ppagejem@smail.uni-koeln.de',
    packages=find_packages('*'),
    install_requires=['pandas', 'yfinance', 'deap', 'numpy', 'scipy', 'ta', 'lxml'],
)

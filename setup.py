from setuptools import setup, find_packages

setup(
    name="SearchPyLinux",  
    version="0.1.1",   
    author="Alberto Emiliani Giorgio Tassinari",   
    author_email="giorgio.programmer@gmail.com", 
    description="A simplyfy search on python",
    long_description="qtag-SearchPyLinux is a search tool designed specifically for humans.",
    url="https://github.com/giorgioGTelian/SearchPyLinux",    
    packages=find_packages(),   
    install_requires=[
        "numpy",   
        "requests",    
    ],
)

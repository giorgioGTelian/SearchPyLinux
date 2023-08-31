from setuptools import setup, find_packages

setup(
    name="SearchPyLinux",  
    version="0.1.0",   
    author="Alberto Emiliani Giorgio Tassinari",   
    author_email="giorgio.programmer@gmail.com", 
    description="A simplyfy search on python",
    long_description="qtag-SearchPyLinux is a search tool designed specifically for humans. It allows for searching files and directories based on tags - words or word beginnings - in any order.
For example, searching with the tag -ari- would match -Aristotle-, my -Arist-, and even -MyFriendArist-, but not -parish-.",
    url="https://github.com/giorgioGTelian/SearchPyLinux",    
    packages=find_packages(),   
    install_requires=[
        "numpy",   
        "requests",    
    ],
)

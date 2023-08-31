import re
import pytest
from qtag import  remove_escapes




def remove_escapes(str):
    new = ''
    for i in range(len(str)):
        if str[i] == '\\' and i < len(str) - 1 and str[i + 1] == '\\':
            new += '\\'
        else:
            new += str[i]
    return new


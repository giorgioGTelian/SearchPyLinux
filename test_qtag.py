import re
import pytest
from qtag import  remove_escapes, try_compile_whole_tag, delete_single_tag

def test_delete_single_tag():
    # Sample data for testing
    match = re.search("tag", "sample_tag_filename.txt")  # A dummy match object
    testfilename = "sample_tag_filename.txt"
    filename = "/path/to/sample_tag_filename.txt"
    tag = "tag"
    linkname = "/path/to/link/sample_tag_filename.txt"
    
    # Call the function with sample data
    new_filename = delete_single_tag(match, testfilename, filename, tag, linkname)
    
    # Check if the 'tag' is deleted from the filename
    assert "tag" not in new_filename
  


def remove_escapes(str):
    new = ''
    for i in range(len(str)):
        if str[i] == '\\' and i < len(str) - 1 and str[i + 1] == '\\':
            new += '\\'
        else:
            new += str[i]
    return new

def test_try_compile_whole_tag():
    regex = try_compile_whole_tag("test", "[", "]")
    # Check if the returned regex is a valid regex pattern object
    assert isinstance(regex, re.Pattern)

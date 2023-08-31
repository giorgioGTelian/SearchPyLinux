# SearchPyLinux qtag version C.07

## Overview:
### qtag is a search tool designed specifically for humans. It allows for searching files and directories based on tags - words or word beginnings - in any order. <br>
### For example, searching with the tag "ari" would match "Aristotle", "my Arist", and even "MyFriendArist", but not "parish".

# Features:
<strong> Tag-based Searching: </strong> Search using tags which are words or word beginnings in any order. <br>
<strong> Negative Tags: </strong>Using a leading colon with a tag allows for an exclusion search. For instance, searching with the tag ":pdf" would exclude files with the tag "pdf". <br>
<strong> Wildcards: </strong>Use the dot (".") as a wildcard for any single character, and ".*" for any sequence of characters. <br>
<strong> Options: </strong>Various options such as searching only directories, files, case-sensitive search, local search, and more. <br>
<strong> Path Setting: </strong>Specify the search path or use the current directory as default. <br>
<strong> Link Creation: </strong>Option to create symbolic links to matching files in a working directory. <br>
<strong> Tag Management: </strong>Add or delete tags from files. <br>
<strong> Verbose Mode: </strong>Match directories as well if the filename does not match. <br>
<strong> Help: </strong>Comprehensive help documentation for usage. <br> 
## How to Use: <br>
### Search: <br>

<strong> Basic Search:</strong> ```qtag [Tags and Options]``` <br>
<strong> Exclusion Search:</strong> ```qtag :[Tag to Exclude]``` <br>
<strong> Combination Search:</strong> ```qtag [Tag1] [Tag2]``` (AND search that matches all tags) <br>
<strong> Wildcard Search:</strong> ```qtag [.*Tag]``` (Wildcard for any sequence of characters before the tag) <br>

### Options:

```-p [path]```: Specify search path.<br>
```-w```: Write links to matching files to working directory and open it in a file manager.<br>
```-a```: Append links to the working directory without overwriting existing links.<br>
```-c```: Case sensitive search.<br>
```-d```: Search only for directories.<br>
```-f```: Search only for files.<br>
```-l```: Local search (no recursion).<br>
```-s```: Simple search (avoid matching embodied tags).<br>
```-x```: Write qtag to .local/bin for quick calling (if .local/bin is in PATH).<br>
```-n``` [tag]: Manage tags (add or delete).<br>
```-r```: Write to disk (only relevant with -n).<br>
```-h```: Print help documentation.<br>

### Set ```qtag``` as a Command:

Use the ```-x ```option to write``` qtag ```to ```.local/bin``` for easy access.

### Output:

Directories are prefixed with "DIR:" in bold.<br>
Matches will be output with their paths.<br>
If the -w or -a option is used, symbolic links to matching files will be created in the working directory.<br>

### Help:

Use the ```-h ```option to view detailed instructions and examples.
### Known Issues:
If the user does not provide any arguments, the tool defaults to displaying the help documentation.
### Future Improvements:
Implement additional functionalities like OR search.
Improve error handling and user feedback.
Optimize searching for better performance on larger datasets.
### Disclaimer:
This tool has been designed for search operations and does not alter or delete user data. Always backup your data before using any new software. The creator of qtag is not responsible for any loss of data or any other unintended consequences.

#!/usr/bin/python3

# This code is distributed under GNU General Public Licence (GPL). See http://www.gnu.org/copyleft/gpl.html

# Version must be updated in last line of class MyDefaults

# Major changes for version C up to C05:
# main REGEXes compiled only once.
# Possibility of listing many options in single string with leading "-"
# Found and corrected a bug about case sensitive search and tag add and del with lower case tag
# Added 0-9 and "," as normal separators.
# Put ig in Defaults, so that it can be modified easily
# When renaming, if trying to rename to name of existing file, ask user whether to add standard tag, to skip renaming or to add another string of her choice
# Fixed bug in delete single tag: if tag is regex, error (of course). Rewritten delete_single_tag more efficiently: comparison with compiled regex of plain tag

# Changes from C05 to C06:
# main loop in scan_all: replaced glob.iglob loop with os.walk loop
# added notag check: if a dir contains a file called "notag", the dir and all its subdirs are cut from the tree and are not scanned

# Changes from C06 to C07:
# In workpathdir, reproduce dir tree, only for the branches that contain file matches. Made relevant changes in correct_filename, delete_single_tag, manage_tag_new,
# which now get in input whole absolute path both for target and for link.
# In append mode, file manager is called.

import sys, os, glob, re, shutil


class Colors:
    Green, Red, White = '\033[92m', '\033[91m', '\033[0m'
    Bold, Italics, Normal = '\033[1m', '\x1B[3m', '\033[0m'


class MyDefaults:
    def __init__(self):
        self.quick = True
        self.case_sensitive = False
        self.recursive = True
        self.onlydirs = False
        self.onlyfiles = False
        self.set_qtag = False
        self.dont_simulate = False
        self.extended = True
        self.writing = 'N'
        self.new_tag = ""
        self.programpath = sys.argv[0]
        self.new_argv = []
        self.negative_list = []
        self.positive_list = []
        self.userpath = './'
        self.workpath = ""
        self.ancient_workdir = False
        self.separators = r'\^\$\*\+\?\{\}\[\]\\\|\(\)\.\-/_ 0123456789'
        self.ig = "[\^\$\*\+\?\{\}\[\]\\\|\(\)\.\-/_, 0-9]"
        self.version = 'qtag vers. C.07'


def begins_uppercase(test):
    if test[0] == test[0].upper():
        return (True)
    else:
        return (False)


def init_writing():
    Defaults.workpathdir = '/0qtag_results'
    Defaults.workpath = os.environ['HOME'] + Defaults.workpathdir  # to find out files in workpath and discard them in scan
    if Defaults.writing == 'Y':
        if os.path.exists(Defaults.workpath):
            shutil.rmtree(Defaults.workpath)
        os.mkdir(Defaults.workpath)
    elif Defaults.writing == 'A':
        if not (os.path.exists(Defaults.workpath)):
            os.mkdir(Defaults.workpath)
        else:
            Defaults.ancient_workdir = True
    else:
        if os.path.exists(Defaults.workpath):
            Defaults.ancient_workdir = True


def look_for_path():
    path_str = os.environ['PATH']
    path_list = path_str.split(':')
    home_path = os.environ['HOME']
    for one_path in path_list:
        if home_path.find(one_path):
            return (one_path)
    else:
        printout_error(
            'No home path found in environ variable PATH\nChange PATH manually or copy qtag to system dir (SU privileges required)')
        sys.exit(0)


def set_qtag_command():
    found_path = look_for_path()
    try:
        if not (os.path.exists(found_path)):
            os.mkdir(found_path)
            print("Created dir", found_path)
    except:
        printout_error("Error creating " + found_path)
        return
    destpath = os.path.join(found_path, 'qtag')
    if destpath == Defaults.programpath:
        printout_error("Error: you are trying to copy " + Defaults.programpath + "\nto " + destpath)
        sys.exit(0)
    try:
        shutil.copy(Defaults.programpath, destpath)
        print()
        print("Copied file", Defaults.programpath, "to", destpath)
        print(Colors.Bold, "'qtag'", " can now be run as a command", sep="")
        print("(To check path: 'echo $PATH')")
    except:
        printout_error("Error copying file qtag to " + destpath)


def pause():
    print(Colors.Normal, 'Press ENTER to continue', Colors.Bold, sep="")
    sys.stdin.read(1)


def print_help():
    print(Colors.Bold, '******* qtag       A search tool for ', Colors.Red, 'HUMANS', Colors.Normal, Colors.Bold,
          ' -- by Alberto Emiliani       *******', sep='')
    print('Computers contrive such file names as "0TR6fE0dr5TW", but humans use WORDS.')
    print('The goal of qtag is to make search for file names written by humans easier.')
    print('TAGS are WORDS OR WORD BEGINNINGS, in any order. Syntax: qtag [Tags and Options]')
    print('"qtag ari" matches "Aristotle", "my Arist", even "MyFriendArist"; NOT "parish".')
    print('Leading colon means NOT. "qtag repo :pdf" finds "Report.doc", not "Report.pdf"')
    print('Any number of tags can be combined for an AND search that matches all of them.')
    print('WILDCARDS: dot (".") stands for any single char; ".*" for any sequence of chars.')
    print('OPTIONS:specify them where you like. "-p","-n" REQUIRE argument. -h prints this.')
    print(Colors.Green, '-p', Colors.Normal, Colors.Bold,
          '      search path. MUST be followed by (space and) userpath. Def.: current dir', sep="")
    print(Colors.Green, '-w', Colors.Normal, Colors.Bold,
          '      write links to matching files to working dir, open it in file manager', sep="")
    print(Colors.Green, '-a', Colors.Normal, Colors.Bold,
          '      write links to working dir but append (add) them to existing links', sep='')
    print(Colors.Green, '-c', Colors.Normal, Colors.Bold, '      case sensitive search', sep='')
    print(Colors.Green, '-d', Colors.Normal, Colors.Bold, '      search only for dirs ', Colors.Green, '-f',
          Colors.Normal, Colors.Bold, ' only for files ', sep='', end='')
    print(Colors.Green, '-l', Colors.Normal, Colors.Bold, ' local search (no recursion)', sep='')
    print(Colors.Green, '-s', Colors.Normal, Colors.Bold,
          '      simple search -- no such embodied tags as: "for" in "LookForMe"', sep='')
    print(Colors.Green, '-x', Colors.Normal, Colors.Bold,
          '      write qtag to .local/bin for quick calling - if .local/bin is in PATH', sep='')
    print('OPTIONS for TAG MANAGEMENT:', Colors.Green, "-n", Colors.Normal, Colors.Bold, ' + -r and options', sep='')
    print('"-n" works on files captured in working dir (by previous -w or -a search)')
    print(Colors.Green, '-n tag', Colors.Normal, Colors.Bold, '  adds tag if not already there                 ',
          Colors.Green, '-n :tag', Colors.Normal, Colors.Bold, '  deletes tag', sep='')
    print(Colors.Green, '-c,-s', Colors.Normal, Colors.Bold,
          ' are effective for deciding if tag is already there (for add or del)', sep='')
    print('-r writes to disk: ALL options other than -r,-c,-s are ignored by "-n"')
    print('*******  ', Defaults.version, '   More help and examples in "qtag.info.txt".    *******', Colors.Normal,
          sep="")


def printout_error(message):
    a = '**********************************************************'
    print(Colors.Red, a, sep="")
    print(message)
    print(a, Colors.Normal)


def try_compile(tag, ig):  # called by cond_check: returns compiled regex
    try:
        regex = "^(" + tag + ")|" + ig + tag
        p = re.compile(regex)  # both test_string and testfilename are original, that is, this is a case sensitive check
    except:
        tag = re.escape(tag)
        printout_error('WARNING: invalid REGEX. Reinterpreting symbols as escaped: ' + tag)
        regex = "^(" + tag + ")|" + ig + tag
        p = re.compile(regex)
    return ([p, tag])


def compile_regexes():  # only for leading tag in word or whole word
    x = 0
    #    ig="[\.\ \-/_,0-9]" # ig means "inner group", groups for testing begin and end word in regex
    igext = Defaults.ig[
            :-1] + "a-z]"  # INNER GROUPS FOR REGEX FOR CASE_SENS AND FOR EXTENDED: ig extended search  IMPORTANT: add 0-9 if taken away from ig

    def append_compiled_regex(tag, positive):
        if not Defaults.case_sensitive and Defaults.extended:  # now compile regex for case sens. and case-ins. extended
            tag = tag[0].upper() + tag[1:].lower()  # normalize tags to find extended tags
        if Defaults.case_sensitive and not begins_uppercase(
                tag):  # if case sens but not beg.with.upper we don't want to match ending parts of words
            compiled_case_sens = try_compile(tag, Defaults.ig)
        else:
            compiled_case_sens = try_compile(tag, igext)  # returns compiled regex in p
        tag = compiled_case_sens[1]
        p1 = compiled_case_sens[0]
        tag = tag.lower()
        p2 = try_compile(tag, Defaults.ig)[0]
        if positive:
            Defaults.positive_list.append([p1, p2])
        else:
            Defaults.negative_list.append([p1, p2])

    while x < (len(Defaults.new_argv)):
        tag = Defaults.new_argv[x]
        if tag[0] == ':':
            tag = tag[1:]
            append_compiled_regex(tag, False)
        else:
            append_compiled_regex(tag, True)
        x += 1


def get_next_arg(argv_index, option):
    if argv_index >= len(sys.argv):
        printout_error("Argument missing after option -" + option)
        sys.exit()
    else:
        return (sys.argv[argv_index])


def set_option(option, argv_index):
    if option == 'c':
        Defaults.case_sensitive = True
    elif option == 'l':  # local
        Defaults.recursive = False
    elif option == 'w':  # write new
        Defaults.writing = 'Y'
    elif option == 'a':  # write append
        Defaults.writing = 'A'
    elif option == 'd':  # dirs only
        Defaults.onlydirs = True
    elif option == 's':  # search only for not embodied tags -- no 'for' in 'CallForHelp'
        Defaults.extended = False
    elif option == 'r':  # really write (for -n)
        Defaults.dont_simulate = True
    elif option == 'f':  # only files
        Defaults.onlyfiles = True
    elif option == 'x':  # write qtag to local/bin
        Defaults.set_qtag = True
    elif option == 'h':  # help
        print_help()
        sys.exit()
    elif option == 'v':  # verbose: matches also if dir matches but not filename
        Defaults.quick = False
    elif option == 'p':  # set search path
        argv_index += 1
        Defaults.userpath = get_next_arg(argv_index, 'p')
        if Defaults.userpath[-1] != '/':
            Defaults.userpath += '/'
        if (Defaults.userpath[0] != '/') and (Defaults.userpath[0] != '.'):  # if relative but not beginning with './'
            Defaults.userpath = './' + Defaults.userpath
        if not (os.path.exists(Defaults.userpath)):
            printout_error('User path "' + Defaults.userpath + '" does not exist, setting it to current directory')
            Defaults.userpath = "./"
    elif option == 'n':  # manage tags
        argv_index += 1
        try:
            Defaults.new_tag = get_next_arg(argv_index, 'n')
        except:
            printout_error("Argument missing after '-n'")
            sys.exit(0)
    else:
        printout_error('Unrecognized option: ' + option)
    return (
        argv_index)  # return index to loop in get_options; +=1 normally but +=2 for 'p' and 'n', which require argument


def get_options(options_string, argv_index):
    counter = 0
    while counter < len(options_string):
        option = options_string[counter]
        argv_index = set_option(option, argv_index)
        counter += 1
    return (
                argv_index + 1)  # for while loop in get_arguments -- options p and n have already incremented argv_index in set_option


def get_arguments():
    argCounter = 0
    x = 1  # 0 has already gone into self.programpath
    while x < (len(sys.argv)):
        if sys.argv[x][0] == '-':
            if len(sys.argv[x]) < 2:
                printout_error("'-' not followed by option")
                sys.exit()
            x = get_options(sys.argv[x][1:].lower(), x)
        else:
            Defaults.new_argv.insert(argCounter, sys.argv[x])
            argCounter += 1
            x += 1
    if (len(sys.argv)) == 1:
        x = get_options("-h", x)  # x is dummy here; if empty string, just printout help
    compile_regexes()  # once you have all the options set and the tags in Defaults.new_argv, compile regexes and put them into their lists


#   #   #   #   #   #   #   #   #   #   #   #   #   #   END OF INITIALIZATION --- BEGINS NORMAL SEARCH 


def output_filename(fname):		# The first part deals with the printing to scr, the second with creating symlinks to matching files in workpathdir
	if os.path.isdir(fname):		# If fname is a dir, we just print "DIR" in bold type
		print(Colors.Bold, 'DIR:', Colors.Normal, sep="", end="")
	if fname[0:2] == './':
		print(fname[2:])
	else:
		print(fname)
	if Defaults.writing == 'N':		# If we don't have to create any symlinks, return
		return
	if (Defaults.userpath[0] == '/'):  # if absolute path in userpath; (userpath is at least "./", so no error here)
		targetname = os.path.abspath(fname)
	else:
		if fname[0:2] == './':  # if filename begins with ./ strip it off
			fname = fname[
					2:]  # no error should be possible here, because function output_filename is only entered with fname != ""
		targetname = os.path.abspath(fname)	#check this: from version C06 every fname should come with absolute path
# In version C7, we re-create dir tree
	# First, let's try to shorten the tree to the current dir:
	shortname=os.path.relpath(targetname,Defaults.userpath)
	if os.path.isdir (shortname):
		if not os.path.exists(os.path.join(Defaults.workpath,shortname)):
			os.makedirs(os.path.join(Defaults.workpath,shortname))
	else:
		head,tail = os.path.split(shortname)
		newdir = os.path.join(Defaults.workpath,head)
		if not os.path.exists(newdir):		
			os.makedirs(newdir)
		link=os.path.join(newdir,tail)
		if not os.path.exists(link):
			os.symlink(targetname,link)




def cond_match(compiled, testfilename, orig_filename, negative):
    # called by cond_check: returns ['m',_] if matches
    # ['n',_] if it does not; [_,""] if cond is not satsf. (match if negative and not match if pos.)
    # [_,filename] if cond is satisf. (match if pos and not match if neg.)
    # 'm' 'n' are needed by cond_check to decide whether to go on if search case_ins. AND extended;
    # in this case, if there is a match the test is complete (ok if pos and failed if neg)
    # otherwise we must go on to test lowercase tag and lowercase filename
    # at any rate, in case of success we return the original file name (not the lowercase one)
    m = compiled.search(testfilename)
    if m:  # if it matches (m) it returns, both if case-sens and if not case-sens but uppercase-first
        if negative:  # the point of this complex structure is that we want to
            return ['m', ""]  # recognize things as "erTag..." "09080Tag..." even for case insensitive search
        else:
            return ['m', orig_filename]
    else:
        if not (negative):  # if it is NOT c-sens. then it's here only if it is uppercase-first but it doesn't match
            return ['n',
                    ""]  # therefore, in this case, the not matching is not a success if negative and not a failure if not negative
        else:  # It is such a success or failure only in case the search was case_sens. -- upper-first or not.
            return ['n', orig_filename]


def cond_check(filename, compiled_regex,
               negative):  # called by check_filename: returns filename if match or "". Calls cond_match.
    # compiled_regex is a list of two elements: (1) regex for extended and case sens search; (2) regex for case ins and not ext. (lowercase) search
    if Defaults.case_sensitive or Defaults.extended:
        result = cond_match(compiled_regex[0], filename, filename, negative)
        if Defaults.case_sensitive or result[0] == 'm':  # if case-sens., ok, test ended, if not
            return result[1]  # test is good only if it matched -- negative or positive (bec. it may still match)
    l_filename = filename.lower()  # but first we lowercase everything
    result = cond_match(compiled_regex[1], l_filename, filename, negative)
    return result[1]  # it came to this point only if it didn't match before. The present result is the good one


def check_filename(
        filename):  # called by scan_all. Loops through compiled regexes, calls cond_check. Returns filename if it matches or "" else
    for compiled_regex in Defaults.positive_list:
        filename = (cond_check(filename, compiled_regex, False))
        if filename == "":
            return ""
    for compiled_regex in Defaults.negative_list:
        filename = (cond_check(filename, compiled_regex, True))
        if filename == "":
            return ""
    return filename


def scan_all():  # called by normal search, not by add or delete tags (-n). Loops through filenames. Calls check_filename. If file matches, prints it and updates counter
	total_number = 0
	match_number = 0  # counter, only for printing number of matching files
	for root,dirs,files in os.walk(Defaults.userpath):
		if Defaults.workpathdir in root:  # in case you are writing or have written to workpath, don't scan workpath too
			continue
		if os.path.isfile(os.path.join(root,"notag")):
			del dirs[:]
			continue
		if not Defaults.onlyfiles:
			for testFilename in dirs:
				total_number += 1
				backname = (check_filename(testFilename))  # ********** crucial line: check the filename, returns filename if check passed or '' else
				if backname != "":
					output_filename(os.path.join(root,testFilename))
					match_number += 1		
		if not Defaults.onlydirs:
			for testFilename in files:
				total_number += 1
				if Defaults.quick:  # if quick flag is set, only check the basename
					shortFilename = os.path.basename(testFilename)
				backname = (check_filename(shortFilename)) 
				# ********** the above is the crucial line: check the filename, returns filename if check passed or '' else
				if backname != "":
					output_filename(os.path.join(root,shortFilename))
					match_number += 1		
		if not Defaults.recursive:
			break

	print()
	print(match_number, "found     ", total_number, "parsed        'qtag -h' for some help")


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   END OF NORMAL SEARCH: BEGINNING OF TAG MANAGEMENT --- -n

def correct_filename(target_whole_name, new_base,linkname):
### DEB	print("*************",new_base)
    # called by delete_single_tag: deletes tag from filename pointed by symlink
    # old=target whole name, new_base=new target name. Also updates symlink.
### DEB	print("***target_whole_name",target_whole_name,"\n","|||new_base",new_base,"\n","|||linkname",linkname)
# non riconosce subdirs in target; new_base va bene, link è solo basename
	head, tail = os.path.split(target_whole_name)
	new = os.path.join(head, new_base)
	print("|||new",new)
	print(Colors.Bold, "renaming", Colors.Normal, target_whole_name, sep="")
	print(Colors.Bold, '      to', Colors.Normal, new, sep="")
	if Defaults.dont_simulate:
		while os.path.exists(new) or os.path.basename(new) == "":
			insert = 'qtag_auto_'
			print(Colors.Red, "WARNING: File already existing or empty name:\n", new, sep='')
			head, tail = os.path.split(new)
			new = os.path.join(head, insert + tail)
			print('Trying to change name to', new, Colors.Normal)
			answer = input('Is this change ok? (y/n OR leading string to add to file) ')
			if answer.lower() == 'n':
				return
			else:
				if answer.lower() != 'y':
					insert = answer
			new = os.path.join(head, insert + tail)
		try:
			os.rename(target_whole_name, new)
		except Exception as e:
			print("**********",e,"||",new)
			printout_error("Cannot rename file")
		try:
			os.remove(linkname)
		except Exception as e:
			print("**********",e)
			printout_error("Unable to remove symlink " + linkname)
		Defaults.writing = 'A'  # to have output_filename write to disk
		output_filename(new)  # update symlink


def remove_escapes(str):  # to remove escape chars from string
    new = ''
    for i in range(len(str)):
        if str[i] == '\\':
            if i < len(str) and str[i + 1] == '\\':
                i += 1
                new += '\\'
        else:
            new += str[i]
    return (new)


def delete_single_tag(match, testfilename, filename, tag,linkname):
# called by manage_new_tag. testfilename=basename of target; filename=whole name of target with abs path
# linkname=whole name of link with abs path
    matching_string = testfilename[match.start():match.end()]  # matching_string is the PART of filenm regex matched.
    # A nice prob here: first char in match may be a separator, but even a char or a digit may be a separator. How do we know if it's a sep. or a part of the match. tag?
    # Best thing: recompile just mere tag and check it against mere matching string. What if search was case insensitive etc.? We then check it lowercase against
    # lowercase matching_string, since lower and case sens and all has already been taken care of before. But there is ONE case in which a minor bug arises.
    # If ext. search for "a" it would match "aAB" but comparison below would remove the former "a". But it would ONLY happen with one-letter searches, AND if first
    # and second letter were identical
    tag = tag.lower()
    test_matching = matching_string.lower()
    p = re.compile(tag)
    result = p.search(test_matching)
    if not result:
        printout_error("Matching string not found in match of regex")
        sys.exit()
    index_start = match.start() + result.start()  # index of first really matching character in filename
    length = result.end() - result.start()
    if len(tag) == 1:  # ok, let's consider special case. If len(tag)==1, min. length of matching string is 1, max is 3 (separators, filename begin and end)
        length = 1
        if len(test_matching) > 1:  # If == 1, all is ok, leave everything as it is. If it's 3, it's the middle one
            if len(test_matching) == 3:
                index_start = match.start() + 1
            else:  # if it's 2: could be tag + sep or sep + tag (the third being file start or end). '<begin>aA' 'aA<end>'
                if test_matching[0] == test_matching[1]:
		# (already lower): go on only if the same letter: otherwise regex comparison already found right one
                    if matching_string[0] != matching_string[1]:  # if == it doesn'matter: ignore case'
                        # and so, we come here only with two equal letters in different case
                        if matching_string[0] == matching_string[0].upper():  # if first is upper, it cannot be separator for second
                            index_start = match.start()
                        else:
                            index_start = match.start() + 1
    index_end = index_start + length  # index of first character after the substring matching tag
    if len(testfilename) > index_end:  # len() = last index of string + 1. If it equals x, index x out of range
        if testfilename[index_end] in ' _-\\':
            index_end += 1
    new_basefilename = testfilename[:index_start] + testfilename[index_end:]
    correct_filename(filename, new_basefilename, linkname)


def try_compile_whole_tag(tag, igb, ige):
    try:
        regex = "^(" + tag + ige + ")|" + igb + tag + ige + "|(" + igb + tag + ")$|^(" + tag + ")$"
        p = re.compile(regex)  # both test_string and testfilename are original, that is, this is a case sensitive check
    except:
        tag = re.escape(tag)
        printout_error('WARNING: invalid REGEX. Reinterpreting symbols as escaped: ' + tag)
        regex = "^(" + tag + ige + ")|" + igb + tag + ige + "|(" + igb + tag + ")$|^(" + tag + ")$"
        p = re.compile(regex)
    return (p)


def cond_check_whole(filename, comp_a,comp_b):
# called by manage_new_tag: returns result of comparison betw. regex, already compiled, and filename
    if Defaults.case_sensitive or Defaults.extended:
        result = comp_a.search(filename)  # returns result of regex search in filename
        if Defaults.case_sensitive or result:  # if case-sens., ok, test ended, if not,
            return (result)  # test is good only if it matched -- negative or positive (lower may still match)
    l_filename = filename.lower()  # fn comes to this point only if case_ins and no match above: first we lowercase filename to perform case_ins search
    return (comp_b.search(l_filename))  # now perform comparison with compiled regex for case_ins -- that is, with tag in lowercase (set by calling fn)


def manage_tag_new(tag,action):
# called by main: for every symlink it calls cond_check_whole to get a match, then accordingly set_new_tag or delete_single_tag or nothing
	counter = 0
	if not os.path.exists(Defaults.workpath):
		printout_error("Working dir " + Defaults.workpath + " missing")
		return
	temp_tag = tag.lower()  # compile regex for case insensitive
	#    ig="[\.\ \-/_,0-9]" # ig means "inner group", groups for testing begin and end word in regex
	comp_case_ins = try_compile_whole_tag(temp_tag, Defaults.ig, Defaults.ig)
	igb = Defaults.ig[
		:-1] + "a-z]"  # INNER GROUPS FOR REGEX FOR CASE_SENS AND FOR EXTENDED: ig begin word  IMPORTANT ADD 0-9 if taken away from ig
	ige = Defaults.ig[
		:-1] + "A-Z]"  # but for tags as whole words: ig end word                              IMPORTANT ADD 0-9 if taken away from ig
	if not Defaults.case_sensitive:  # now compile regex for case sens. and case-ins. extended
		if Defaults.extended:  # case ins extended srch=case sens wt upper first letter
			temp_tag = tag[0].upper() + tag[1:].lower()  # normalize tags to find extended tags
		else:
			temp_tag = ""  # case insensitive and not extended: following regex is not being used in cond_check_whole
	else:  # here only if case_sensitive
		temp_tag = tag
		if not begins_uppercase(tag):
			igb = Defaults.ig
	comp_case_sens = try_compile_whole_tag(temp_tag, igb, ige)  # returns compiled regex in p
	for root, dirs, linknames in os.walk(Defaults.workpath):	# new loop version from C07, recurs through dirs in workpath
		for linkname in linknames:
			link_whole_name=os.path.join(root,linkname)
			target_whole_filename = os.path.realpath(link_whole_name)
#			print("||||manage_tag_new",target_whole_filename,"***",link_whole_name)
			target_basename = os.path.basename(target_whole_filename) # Just test the bare filename, not the path
			result = cond_check_whole(target_basename, comp_case_sens,comp_case_ins)  # we make the actual check, some little log. complexity in it
			if result:
				if action == 'delete_tag':  # you del the tag since it's there, because result ok
					delete_single_tag(result, target_basename, target_whole_filename, tag, link_whole_name)
					counter += 1
					continue
			else:
				if action == 'add_tag':  # result == none: and so you add the tag since it isn't there
					head, tail = os.path.split(target_whole_filename)
					new_base = tag + '_' + tail
	# new tag is added at the beginning of file name, followed by underscore
					correct_filename(target_whole_filename, new_base, link_whole_name)
					counter += 1


	if action == 'add_tag':
		print('\nAdded tag "', tag, '" to ', counter, ' file(s)', sep="")
	else:
		print('\nDeleted tag "', tag, '" in ', counter, ' file(s)', sep="")


def print_debug_info():
    print("case_sensitive", Defaults.case_sensitive)
    print("recursive", Defaults.recursive)
    print("writing", Defaults.writing)
    print("onlydirs", Defaults.onlydirs)
    print("onlyfiles", Defaults.onlyfiles)
    print("set_qtag", Defaults.set_qtag)
    print("path =", Defaults.userpath)
    print("new_tag = '", Defaults.new_tag, "'", sep="")
    print("argv", sys.argv)
    print("Defaults.programpath", Defaults.programpath)
    print("new_argv", Defaults.new_argv)

def main():
    Defaults = MyDefaults()
    get_arguments()
    init_writing()
    print()
    print("*******", Defaults.programpath, "*******")
    print()
    if Defaults.set_qtag:
        set_qtag_command()
        sys.exit(0)
    if Defaults.new_tag != "":
        if Defaults.new_tag[0] == ':':
            manage_tag_new(Defaults.new_tag[1:], 'delete_tag')
        else:
            manage_tag_new(Defaults.new_tag, 'add_tag')
    else:
        scan_all()
    #if not Defaults.ancient_workdir:
    if Defaults.writing != 'N':
        os.system("xdg-open " + Defaults.workpath)
    print(Defaults.version)

if __name__ == "__main__":
    main()


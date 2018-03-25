import re

def imatch(pattern, line):
    pattern = re.compile(pattern, re.IGNORECASE)
    if re.match(pattern, line): return True
    else:                       return False

def matchf(input, pattern, type="s"):
    """
    matchf(imput, input_pattern, [type="s/r"])
        input = String in question
        input_pattern = Pattern against which to match input
        type = Pattern is in the form of a (s)tring or a (r)egex pattern

    Returns only True or False 
    
    Pattern is based LOOSELY on the printf formatting characters. 
        %C = Any number of letters, excluding digits and whitespace
        %c = ONE AND ONLY ONE letter excluding digits and whitespace
        %S = An unlimited string of letters and/or digits, excluding 
             non-alphanumeric characters (such as punctuation and whitespace)
        %s = ONE AND ONLY ONE letter or digit excluding non-alphanumeric 
             characters
        %D = An unlimited string of digits excluding letters
        %d = ONE AND ONLY ONE digit (single digit character, no decimals), 
             excluding letters
        %W/%w = any number of whitespace. There is functionally no difference
                between capital and small %w, however both are used for 
                method consistency. 
        *  = An unlimited string of any character

    Other characters of <input_pattern> are matched exactly. I.e. /dev/A12d*
    is matched as "/dev/A12d" (including capitals) plus any number of following 
    characters
    
    I.e.
    return = matchf(my_string, /dev/disk/%c%c%c%c-*")
    /dev/disk/scsi-2hgd76543jge76r434 will match 
    /dev/dIsk/scsi-2hgd76543jge76r434 will NOT match 
    /dev/disk/scsi- will match 
    /dev/disk/scsi will NOT match 
    
    Be careful to escape any normal string and regex symbols
    """
    # Put the leader in what will be the ultimate search string
    regex_str = str("^")
    # If type is not "s", then the regex string was entered directly as 
    # pattern. No further processing is necessary
    if type.lower() == "s":
        # Parse through the string of pattern one character at a 
        # time. Use % as delimiters. There will ALWAYS be a single character 
        # after a %, so any characters beyond %X are considered literals if
        # they are not another %.
        flag = False # Off
        for inst in str(pattern):
            inst = str(inst)
            if inst == "%":
                flag = True #On
                continue
            if flag is True:
                if   inst == "D":regex_str = regex_str + "[0-9]{1,}"
                elif inst == "d":regex_str = regex_str + "[0-9]{1}"                 
                elif inst == "S":regex_str = regex_str + "[a-zA-Z0-9\.]{1,}"
                elif inst == "s":regex_str = regex_str + "[a-zA-Z0-9\.]{1}"
                elif inst == "C":regex_str = regex_str + "[a-zA-Z]{1,}"
                elif inst == "c":regex_str = regex_str + "[a-zA-Z]{1}"
                elif inst == "W":regex_str = regex_str + "[\s]{0,}"
                elif inst == "w":regex_str = regex_str + "[\s]{0,}"
                flag = False # Off
            else: 
                if inst == "*": regex_str = regex_str + ".{0,}"
                elif inst == ".": regex_str = regex_str + "\."
                else: regex_str = regex_str + str(inst)
        regex_str = regex_str + "$" # Close regex string
    elif type.lower() == "r":
        regex_str = pattern
    else:
        e = "Parameter 'type' is invalid.\n"
        e = e + "Please use 's' for string or 'r' for regex pattern."
        e = e + "type passed was: " + str(type)
        raise ValueError(e)

    # Check pattern and create return  
    if re.match(regex_str, input): return True
    else: return False

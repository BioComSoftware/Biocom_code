def check_str_format(match_pattern, type="s"):
    """
    check_str_format(match_pattern[type="s/r"])
        input_pattern = Required pattern for input
        type = Pattern is in the form of a (s)tring or a (r)egex pattern
        
    Prompts the user for input in the format of <input_aattern>.
    Is based LOOSELY on the printf formatting characters. 
        %C = Any number of letters, excluding digits
        %c = ONE AND ONLY ONE letter excluding digits
        %S = An unlimited string of letters and digits, excluding 
             non-alphanumeric characters (such as punctuation and whitespace)
        %s = ONE AND ONLY ONE letter or digit excluding non-alphanumeric 
             characters
        %D = An unlimited string of digits excluding letters
        %d = ONE AND ONLY ONE digit (single digit character, no decimals), 
             excluding letters
        *  = An unlimited string of any character

    Other characters of <input_pattern> are matched exactly. I.e. /dev/A12d
    is matched as "/dev/A12d" including capitals
    
    Prompt request will loop until acceptable input is received 
    or until SIGINT ("CTRL-c").


    I.e.
    return = check_str_format("/dev/disk/%c%c%c%c-*")
    
    Please enter data in the format: 
    [/dev/disk/????-*]:

    entering /dev/disk/scsi-2hgd76543jge76r434 will match 
    entering /dev/dIsk/scsi-2hgd76543jge76r434 will NOT match 
    entering /dev/disk/scsi- will match 
    entering /dev/disk/scsi will NOT match 
    
    Be careful to escape any normal string and regex symbols
    
    return = check_str_format("\(%d%d%d\)-%d%d%d-%s")

    Please enter data in the format: 
    [(###)-###-[?*]]:
    entering (123)-456-pythonic will match
    entering (123)-456-pythonic123 will NOT match
    entering \(123\)-456-pythonic will NOT match
    entering 123-456-pythonic will NOT match
    
    Other examples ...
    /dev/scsi-*%d = /dev/scsi-[unlimited chars/nums] but must end in a digit
    My Name is %s = My Name is [unlimited letters only]
    test * (test<SPACE>*) = test with mandatory space and anything else after
    """
        
#    literal_tag = Lsep 
#    literal_pattern = ("(.*?)(" + str(literal_tag) + ".*?" +str(literal_tag) + ")(.*)")
#    p = re.compile(literal_pattern)
#    input_list = ["","","",match_pattern]
#    literal_result_list = []
    regex_string = "^"

#    Split string by quotes character (if any) and put into list
#    while len(input_list[0])==0 and len(input_list[3]) > 0 :
#       input_list = p.split(input_list[3])
#       if len(input_list[0]) > 0 :
#          literal_result_list.append(input_list[0])
#       else :
#          literal_result_list.append(input_list[1])
#          literal_result_list.append(input_list[2])
#          
    if type.lower() == "s": result_list = [match_pattern]
        for instance in result_list:
            # Build the regex instance, this will be used to match
            # THESE CHECKS MUST BE DONE IN THIS ORDER
            instance = instance.replace("%D" , "[0-9]{1,}")
            instance = instance.replace("%d", "[0-9]{1}")
            instance = instance.replace("%s", "[a-zA-Z0-9\.]{1}")
            instance = instance.replace("%S", "[a-zA-Z0-9\.]{1,}")
            instance = instance.replace("%c", "[a-zA-Z]{1}")
            instance = instance.replace("%C", "[a-zA-Z]{1,}")
            instance = instance.replace("*", ".*")
            
            # Add the modified instances to the final strings
            regex_string = regex_string + str(instance)
        
        # Close regex string
        regex_string = regex_string + "$"
    elif type.lower() == "r":
        regex_string = match_pattern
        if prompt is None:
            prompt_string = str(match_pattern)
    else:
        e = "Parameter 'type' is invalid.\n"
        e = e + "Please use 's' for string or 'r' for regex pattern."
        e = e + "type passed was: " + str(type)
        print e
        return None
#        raise Exception(e)
    # Gather actual input
    loop = True
#    prompt_string = ( "\nPlease enter data in the format... \n" + 
    prompt_string = ("\n" + str(prompt_string) + "\n" + 
                      "[CTRL-c to quit]:")
    while loop:
        try:
            input = raw_input(prompt_string)
            if re.match(regex_string, input):
                return input
            else:
                print "Invalid format."
        except KeyboardInterrupt, e:
            return None

if __name__ == "__main__":
    pass
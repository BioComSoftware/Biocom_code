def sanitize(_input, blacklist=[], whitelist=[]):
    """
    sanitize(input, [<blacklist>], [<whitelist>])
    
    Cleans any input removing characters included in <blacklist> and
    allowing any characters in <whitelist>.
    
    <blacklist> and <whitelist> must be a list []
    
    Default blacklist is whitespace and ";" (semi-colon). The semi-colon cannot 
    be overridden (allowed) by including it in <whitelist>.
    There is no default whitelist
    
    Escape characters are allowed in lists (I.e. "\t" for tab)
    """
    # disallowed_commands_list CANNOT be overidden by whitelist
    disallowed_commands_list = [";", 
                                "rm ", # A space MUST follow 
                                "chroot ", # A space MUST follow 
                                "cd ",  # A space MUST follow 
                                "eval ",  # A space MUST follow 
                                "eval(",
                                "exec ",  # A space MUST follow 
                                "exec( ", 
                                "su ", # A space MUST follow 
                                "su -", 
                                "sudo ", # A space MUST follow
                                "bash ", # A space MUST follow
                                "bash(",
                                "sh ", # A space MUST follow
                                "sh(",
                                "csh ", # A space MUST follow
                                "csh(", 
                                "tsh ", # A space MUST follow
                                "tsh(",
                                "halt ", # A space MUST follow
                                "shutdown ", # A space MUST follow
                                "init ", # A space MUST follow
                                "chown ", # A space MUST follow
                                "chmod ", # A space MUST follow
                                "reboot ", # A space MUST follow
                                ]
    # Disallowed_list CAN be overidden
    disallowed_list =  [" ",
                        "\t"]
    if blacklist == []:
        blacklist = disallowed_list
    for command in disallowed_commands_list:
        _input = _input.replace(str(command), "")
    for disallowed in blacklist:
        if disallowed not in whitelist:
            _input = _input.replace(str(disallowed), "")
    return _input
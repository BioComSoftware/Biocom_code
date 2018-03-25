def groupiter(iterator, count):
    """
    DESCRIPTION
    groupiter(data, count)
        data  = Set to be iterated over
        count = Number of items to pull out in one loop 
    
    EXAMPLE
        dataset = ['Nausori', 5, True, 
                   'Namadi', 10, True, 
                   'Lautoka', 8, False, 
                   'Suva', 3, True]
        for place, value, truth in groupiter(dataset, 3):
            (...)
            
    THANKS TO
        http://code.activestate.com/recipes/439095-iterator-to-return-items-n-at-a-time/
    """
    itr = iter(iterator)
    while True:
        yield tuple([itr.next() for i in range(count)])
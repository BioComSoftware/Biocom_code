from HTMLParser import HTMLParser
from nltk import clean_html as cleanHTML


def _cleanString(data,
                 allowed = None, 
                 disallowed = None):

    data = str(data)
    data = cleanHTML(data)
    data = HTMLParser().unescape(data)            

    if allowed is not None:
        data = "".join(c for c in data if re.match(allowed, c))
        
    if disallowed is not None:
        data = "".join(c for c in data if not re.match(allowed, c))

    data = data.lstrip()
    data = data.rstrip()
        
    return data    
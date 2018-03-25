##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

def http_error_codes(x):
    """"""
    if (x is None): return "Invalid HTML return code: '" + x + "'"
    
    x = ''.join(c for c in str(x) if c in '1234567890')
    
    if (len(x) < 1): return "Invalid HTML return code: '" + x + "'"
    
    try:
        y = int(x)
    except ValueError as e:
        y = 0

    if (y < 100) or (y > 599): 
        return "Invalid HTML return code: '" + x + "'"

    elif (
        (y >= 103 and y <= 199)  or
        (y >= 209 and y <= 225)  or
        (y >= 227 and y <= 299)  or
        (y >= 309 and y <= 399)  or
        (y >= 418 and y <= 420)  or
        (y == 430 )               or
        (y >= 432 and y <= 499)  or
        (y == 509)                or
        (y >= 512 and y <= 599)  
        ):
        return 'Unassigned'
        
    else:
        return {
        '100':'Continue,"[RFC7231, Section 6.2.1]"',
        '101':'Switching Protocols,"[RFC7231, Section 6.2.2]"',
        '102':'Processing,[RFC2518]',
#         '103-199':'Unassigned',
        '200':'OK,"[RFC7231, Section 6.3.1]"',
        '201':'Created,"[RFC7231, Section 6.3.2]"',
        '202':'Accepted,"[RFC7231, Section 6.3.3]"',
        '203':'Non-Authoritative Information,"[RFC7231, Section 6.3.4]"',
        '204':'No Content,"[RFC7231, Section 6.3.5]"',
        '205':'Reset Content,"[RFC7231, Section 6.3.6]"',
        '206':'Partial Content,"[RFC7233, Section 4.1]"',
        '207':'Multi-Status,[RFC4918]',
        '208':'Already Reported,[RFC5842]',
#         '209-225':'Unassigned',
        '226':'IM Used,[RFC3229]',
#         '227-299':'Unassigned',
        '300':'Multiple Choices,"[RFC7231, Section 6.4.1]"',
        '301':'Moved Permanently,"[RFC7231, Section 6.4.2]"',
        '302':'Found,"[RFC7231, Section 6.4.3]"',
        '303':'See Other,"[RFC7231, Section 6.4.4]"',
        '304':'Not Modified,"[RFC7232, Section 4.1]"',
        '305':'Use Proxy,"[RFC7231, Section 6.4.5]"',
        '306':'(Unused),"[RFC7231, Section 6.4.6]"',
        '307':'Temporary Redirect,"[RFC7231, Section 6.4.7]"',
        '308':'Permanent Redirect,[RFC7538]',
#         '309-399':'Unassigned',
        '400':'Bad Request,"[RFC7231, Section 6.5.1]"',
        '401':'Unauthorized,"[RFC7235, Section 3.1]"',
        '402':'Payment Required,"[RFC7231, Section 6.5.2]"',
        '403':'Forbidden,"[RFC7231, Section 6.5.3]"',
        '404':'Not Found,"[RFC7231, Section 6.5.4]"',
        '405':'Method Not Allowed,"[RFC7231, Section 6.5.5]"',
        '406':'Not Acceptable,"[RFC7231, Section 6.5.6]"',
        '407':'Proxy Authentication Required,"[RFC7235, Section 3.2]"',
        '408':'Request Timeout,"[RFC7231, Section 6.5.7]"',
        '409':'Conflict,"[RFC7231, Section 6.5.8]"',
        '410':'Gone,"[RFC7231, Section 6.5.9]"',
        '411':'Length Required,"[RFC7231, Section 6.5.10]"',
        '412':'Precondition Failed,"[RFC7232, Section 4.2]"',
        '413':'Payload Too Large,"[RFC7231, Section 6.5.11]"',
        '414':'URI Too Long,"[RFC7231, Section 6.5.12]"',
        '415':'Unsupported Media Type,"[RFC7231, Section 6.5.13][RFC-ietf-httpbis-cice-03, Section 3]"',
        '416':'Range Not Satisfiable,"[RFC7233, Section 4.4]"',
        '417':'Expectation Failed,"[RFC7231, Section 6.5.14]"',
#         '418-420':'Unassigned',
        '421':'Misdirected Request,"[RFC7540, Section 9.1.2]"',
        '422':'Unprocessable Entity,[RFC4918]',
        '423':'Locked,[RFC4918]',
        '424':'Failed Dependency,[RFC4918]',
        '425':'Unassigned',
        '426':'Upgrade Required,"[RFC7231, Section 6.5.15]"',
        '427':'Unassigned',
        '428':'Precondition Required,[RFC6585]',
        '429':'Too Many Requests,[RFC6585]',
#         '430':'Unassigned',
        '431':'Request Header Fields Too Large,[RFC6585]',
#         '432-499':'Unassigned',
        '500':'Internal Server Error,"[RFC7231, Section 6.6.1]"',
        '501':'Not Implemented,"[RFC7231, Section 6.6.2]"',
        '502':'Bad Gateway,"[RFC7231, Section 6.6.3]"',
        '503':'Service Unavailable,"[RFC7231, Section 6.6.4]"',
        '504':'Gateway Timeout,"[RFC7231, Section 6.6.5]"',
        '505':'HTTP Version Not Supported,"[RFC7231, Section 6.6.6]"',
        '506':'Variant Also Negotiates,[RFC2295]',
        '507':'Insufficient Storage,[RFC4918]',
        '508':'Loop Detected,[RFC5842]',
#         '509':'Unassigned',
        '510':'Not Extended,[RFC2774]',
        '511':'Network Authentication Required,[RFC6585]',
#         '512-599':'Unassigned',
    }.get(x, 'Unknown HTTP return code.')

if __name__ == '__main__':
    print http_error_codes('baloney')
    print http_error_codes(19)

    print http_error_codes(199)
    print http_error_codes('413')
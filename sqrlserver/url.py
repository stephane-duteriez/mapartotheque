from .nut import Nut
from .utils import pad, depad
import time
import urllib.parse
from base64 import urlsafe_b64encode, urlsafe_b64decode

class Url(object):
    """Represents the SQRL URL that identifies SQRL endpoints

    Args:
        authority (string) : The authority part of the url the SQRL
            client will contact to authenticate. Includes the username,
            password, domain, and port. See RFC 3986, Jan 2005, section
            3.2 (https://tools.ietf.org/html/rfc3986#section-3.2)
        secure (bool) : If True, uses the ``sqrl`` scheme, otherwise
            it uses ``qrl``. Defaults to True.

    Returns:
        Url : The initial Url object
    """

    def __init__(self, authority, secure=True):
        self.authority = authority
        self.secure = secure

    def generate(self, path, **kwargs):
        """Generates the actual URL

        Args:
            path (string) : The path portion of the URL. Must not contain
                any query parameters and must be absolute.

        Keyword Args:
            counter (uint) : The counter you wish to encode into the new nut
                (assuming you didn't provide one). Required if a nut is to
                be autogenerated.
            ext (uint) : The number of characters in the path that the SQRL
                client should include as part of the formal server ID.
                Default is 0.
            ipaddr (string) : The IPv4 or IPv6 you wish to encode into the
                new nut (assuming you didn't provide one). Defaults to '0.0.0.0'.
            key (bytes) : The 32-byte key with which to encrypt the new
                nut (assuming you didn't provide one). Required if a nut is
                to be autogenerated.
            nut (Nut) : The nut you wish to embed in the URL. If omitted,
                one will be generated for you.
            query (list) : Array of tuples, each representing additional
                name-value pairs that will be appended to the SQRL url.
            timestamp (uint) : The UNIX timestamp (seconds only) you wish 
                to encode into the new nut (assuming you didn't provide one).
                Defaults to current system time.
            type (string) : Either 'qr' or 'link'. Defaults to 'qr'.
                Used for setting the link type flag in the new nut.

        Returns:
            string : A string representing a valid SQRL URL
        """

        #path
        assert path[0] == '/'
        assert '&' not in path
        assert '?' not in path

        #nut
        nut = None
        if 'nut' in kwargs:
            assert isinstance(kwargs['nut'], Nut)
            nut = kwargs['nut']
        else:
            assert 'key' in kwargs
            nut = Nut(kwargs['key'])
            assert 'counter' in kwargs
            ipaddr = '0.0.0.0'
            if 'ipaddr' in kwargs:
                ipaddr = kwargs['ipaddr']
            timestamp = time.time()
            if 'timestamp' in kwargs:
                timestamp = kwargs['timestamp']
            nut.generate(ipaddr, kwargs['counter'], timestamp=timestamp)
        assert nut is not None
        flag = 'qr'
        if 'type' in kwargs:
            flag = kwargs['type']
        nutstr = nut.toString(flag)

        #query
        query = []
        if 'query' in kwargs:
            query = kwargs['query']
        if ( ('ext' in kwargs) and (kwargs['ext'] is not None) and (kwargs['ext'] > 0) ):
            query.insert(0, ('x', kwargs['ext']))
        query.insert(0, ('nut', nutstr))

        #build
        parts = []
        if self.secure:
            parts.append('sqrl')
        else:
            parts.append('qrl')
        parts.append(self.authority)
        parts.append(path)
        parts.append(None)
        parts.append(urllib.parse.urlencode(query, doseq=True))
        parts.append(None)

        return urllib.parse.urlunparse(parts)

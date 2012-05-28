import hashlib
import re
import types
import unidecode
import uuid


def plural_name(name):
    if name[-1] == 'y':
        return "{}ies".format(name[:-1])
    else:
        return "{}s".format(name)


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """ Returns a bytestring version of 's', encoded as specified in
        'encoding'. If strings_only is True, don't convert (some)
        non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


def get_hexdigest(salt, raw_password):
    """ Returns a string of the hexdigest of the given plaintext password and salt
        using the sha1 algorithm.
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    return hashlib.sha1(salt + raw_password).hexdigest()


def slugify(text, separator='-', prefix=True):
    text = unidecode(smart_str(text))
    text = re.sub('[^\w\s]', '', text)
    text = re.sub('[^\w]', separator, text)
    if prefix:
        hsh = uuid.uuid4().hex[:4]
        text = '%s%s%s' % (text, separator, hsh)
    return text.lower()

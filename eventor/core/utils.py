import re
import types
from unidecode import unidecode
import uuid
from datetime import datetime
from os.path import abspath, dirname, join
from flask import json


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.ctime()
        return super(CustomEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, indent=2, cls=CustomEncoder)


def plural_name(noun, language='en'):
    """ pluralize a noun for the selected language
    """
    for applyRule in rules(language):
        result = applyRule(noun)
        if result:
            return result


def rules(language):
    """ helper method for getting plural form rules from the text file
    """
    rule_file = join(dirname(abspath(__file__)), 'rules.%s') % language
    for line in file(rule_file):
        pattern, search, replace = line.split()
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)


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


def slugify(text, separator='-'):
    text = unidecode(smart_str(text))
    text = re.sub('[^\w\s]', '', text)
    text = re.sub('[^\w]', separator, text)
    return text.lower()


def underscorize(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

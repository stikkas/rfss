import os
from hashlib import md5
from time import time


def is_ascii(str):
    return all(ord(char) < 128 for char in str)

def upload_to(instance, filename):
    # Fix md5 trouble with unicode
    filename = filename if is_ascii(filename) else filename.encode('utf-8')

    # Make file name
    ext = os.path.splitext(filename)[1].lower()
    name = '%d-%s%s' % (time(), md5(filename).hexdigest()[:5], ext)

    # Make relative path from MEDIA_ROOT
    basedir = os.path.join(instance._meta.app_label, instance._meta.module_name)

    # Make subdirectory in basedir
    subdir = md5(name).hexdigest()[:2]

    return os.path.join(basedir, subdir, name)

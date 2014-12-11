# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# __init__.py
#------------------------------------------------------------------------------

import urllib3.request
import urllib3.exceptions



def isServerOn(f):
    def wrapper(*args):
        cls  = args[0]
        uri = 'http://%(host)s:%(port)s/solr' % cls.__dict__
        try:
            response = urllib3.request.urlopen(uri)
            if response.getcode() == 200:
                print('Bingo')
            else:
                print('The response code was not 200, but: {}'.format(
                    response.get_code()))
        except urllib3.exceptions.HTTPError as e:
            print('''An error occurred: {}
            The response code was {}'''.format(e, e.getcode()))

    return wrapper



from django_template_introspection import GLOBALS
import re
import os
import json
from settings import DTI_DEBUG, DTI_INSERT_FILES, DTI_PATH


def read_scripts(fname):
    """ Reads the content of the scripts and formats the insertion"""
    fil = open(os.path.join(DTI_PATH, fname), 'r')
    content = fil.read()
    fil.close()
    if fname.endswith('.js'):
        return '<script type="text/javascript">' + content + '</script>'
    elif fname.endswith('.css'):
        return '<style type="text/css" /> ' + content + '</style>'
    else:
        return content


class TemplateIntrospect(object):
    """ Template introspection middleware that flushes local thread storage
        and inserts new provanence traces of the html-tags
        into produced output with the scripts to navigate over then"""

    def process_request(self, request):
        """ Create an empty meta-data storage, if we are in DTI_DEBUG """
        if not DTI_DEBUG:
            return

        GLOBALS.tdebug = {}
        #GLOBALS.request = request
        #GLOBALS.user = getattr(request, 'user', None)

    def process_response(self, request, response):
        """ Inject meta-data & javascripts to navigate it
            into resulting HTML output """
        if not DTI_DEBUG:
            return response

        content = response.content
        head = re.search(u"</head", content, re.I)
        if head:
            index = head.start()
        else:
            #This is not a valid HTML output (css, js etc.),
            #we should not change its content!
            return response
        response.content =  content[:index] + \
                            self.form_introspec_data() + \
                            content[index:]
        return response

    @staticmethod
    def form_introspec_data():
        """ Format insetion block """
        return '<script type="text/javascript"> var dhash= %s; </script>' % json.dumps(GLOBALS.tdebug) + \
               reduce(lambda x,y: x + '\n' + y, [read_scripts(i) for i in DTI_INSERT_FILES])

from django_template_introspection import GLOBALS
#from django.conf import settings
import re, os, json

INSERT_FILES = ('js/insertion.html', 
                'js/jquery.jgrowl_minimized.js', 
                'js/jquery.jgrowl.css')

class TemplateIntrospect(object):
    """ Template introspection middleware 
        flushes metadata storage and
        inserts new metadata with navigational scripts
        into produced HTML output"""
 
    def process_request(self, request):
        """ Create empty meta-data storage """
        GLOBALS.tdebug = {}
        #GLOBALS.request = request
        #GLOBALS.user = getattr(request, 'user', None)

    def process_response(self, request, response):
        """ Inject meta-data & javascripts to navigate it
            into resulting HTML output """
        content = response.content
        head = re.search(u"</head", content, re.I)
        if head:
            index = head.start()
        else:
            return response
        response.content =  content[:index] + \
                            self.form_introspec_data() + \
                            content[index:]
        return response 

    @staticmethod
    def form_introspec_data():
        """ Format insetion block """
        def read(fname):
            path = os.path.dirname(__file__) 
            fil = open( os.path.join(path, fname) , 'r')
            content = fil.read()
            fil.close()
            if fname.endswith('.js'):
                return '<script type="text/javascript">' + content + '</script>'
            elif fname.endswith('.css'):
                return '<style type="text/css" /> ' + content + '</style>'
            else:
                return content
        return '<script type="text/javascript"> var dhash=' + \
               json.dumps(GLOBALS.tdebug) + \
               '; </script>' + \
               reduce(lambda x,y: x+'\n'+y, [read(i) for i in INSERT_FILES])



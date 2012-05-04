from django_template_introspection import GLOBALS
#from django.conf import settings
import re, os, json

#tempates of the bits that will be inserted into produced template
INSERT_FILES = ('js/insertion.html', 
                'js/jquery.jgrowl_minimized.js', 
                'js/jquery.jgrowl.css')
PATH = os.path.dirname(__file__) 

def read_scripts(fname):
    """ Reads the content of the scripts and formats the insertion"""    
    fil = open( os.path.join(PATH, fname) , 'r')
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
        """ Create an empty meta-data storage """
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
        bindings_template = \
            '<script type="text/javascript"> var dhash= %(bindings)s; </script>' + \
            reduce(lambda x,y: x+'\n'+y, [read(i) for i in INSERT_FILES])
        return bindings_template % { 'bindings' : json.dumps(GLOBALS.tdebug)



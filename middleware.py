from django_template_introspection import globals
from django.conf import settings
import re, os, json

insert_files = ('js/insertion.js', 'js/jquery.jgrowl_minimized.js', 'js/jquery.jgrowl.css')

class TemplateIntrospect(object):
    #create empty meta-data storage
    def process_request(self, request):
        globals.tdebug={}
        #globals.request = request
        #globals.user = getattr(request, 'user', None)

    #inject meta-data & javascripts to navigate it into resulting HTML output
    def process_response(self, request, response):
        content = response.content
        head = re.search(u"</head", content, re.I)
        if head:
            index = head.start()
        else:
            return response
        response.content =  content[:index] + self.form_introspec_data() + content[index:]
        return response 

    #format insetion block
    @staticmethod
    def form_introspec_data():
        def read(fname):
            path = os.path.dirname(__file__) 
            f = open( os.path.join(path, fname) , 'r')
            content = f.read()
            f.close()
            return content
        return '<script type="text/javascript"> var dhash=' + \
               json.dumps(globals.tdebug) + \
               '; </script>' + \
               reduce(lambda x,y: x+'\n'+y, [read(i) for i in insert_files])



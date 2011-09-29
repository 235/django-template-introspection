from django_template_introspection import globals
from django.conf import settings
import re, os, json

class TemplateIntrospect(object):
    def process_request(self, request):
        #globals.request = request
        #globals.user = getattr(request, 'user', None)
        globals.tdebug={}

    def process_response(self, request, response):
        content = response.content
        head = re.search(u"</head", content, re.I)
        #index = head.start() if head else 0
        if head:
            index = head.start()
        else:
            return response
        response.content =  content[:index] + self.form_introspec_data() + content[index:]
        return response 

    def form_introspec_data(self):
        def read(fname):
            path = os.path.dirname(__file__) 
            f = open( os.path.join(path, fname) , 'r')
            content = f.read()
            f.close()
            return content
        insertion = read('js/insertion.js')
        tip = read('js/jquery.jgrowl_minimized.js')
        tipcss = read('js/jquery.jgrowl.css');
        return '<script type="text/javascript"> var dhash=' +  json.dumps(globals.tdebug) + '; </script>' + insertion + tip + tipcss


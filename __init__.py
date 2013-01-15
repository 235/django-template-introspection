from settings import DTI_DEBUG, DTI_TRACE_TEMPLATE
from django.conf import settings
from django.template import Template, StringOrigin
from BeautifulSoup import BeautifulSoup, Tag
from hashlib import md5
import inspect, os
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

#Create a global variable that will be visible in a modified template render 
#here we store all provanence traces of the produced output
GLOBALS = local()

#Collect paths to modules that have to be excluded from a trace tree: 
#exclude django & the current module
import django
EXCLUDE_PATHS = (django.__file__.split('__init__')[0] , 
                 __file__.split('__init__')[0] )


###Django template engine monkey-patching
#we enable provanence collection in its runtime
def enhanced_init(old_init):
    """ Decorator over the original init in order to store the template name """
    def new_init(self, template_string, origin=None, name='<Unknown Template>'):
        if origin is None:
            self.origin = StringOrigin(template_string)
        else:
            self.origin = origin
        return old_init(self, template_string, origin, name)
    return new_init

def render(self, context):
    """ New render that saves metadata and annotate produces tags """
    def nice_inspect():
        """ Inspect the trace tree, collect usuful data """
        tree = []
        frame = inspect.currentframe().f_back
        #skip excluded and only then gather few hops
        while frame.f_back and frame.f_code.co_filename.startswith(EXCLUDE_PATHS):
            frame = frame.f_back
        for i in range(1, 3):
            if frame.f_code.co_filename.startswith(EXCLUDE_PATHS):
                frame = frame.f_back
                continue
            trace = inspect.getframeinfo(frame)
            filename = os.path.relpath(trace.filename, settings.SITE_BASEDIR)
            formatted = DTI_TRACE_TEMPLATE % { 'file': filename, 
                                           'line': trace.lineno, 
                                           'func': trace.function, 
                                           'code': "<br/>".join(trace.code_context)}
            tree.append( formatted.replace("'", '"') )
            frame = frame.f_back
        return tree

    def insert_metadata(tree, output):
        """ Add current rendering event to the global metadata, annotate output """
        info = {'origin': os.path.relpath(str(self.origin), settings.SITE_BASEDIR),
                #'name':   str(self.name),
                'tree': "<br/>".join(tree)}
        dhash = md5(str(info['origin'])).hexdigest()
        GLOBALS.tdebug[dhash] = info

        #add an attribute to each HTML-tag with a given hash or update existing
        #WARNING: if the produced HTML is invalid, BeautifulSoup will try to fix it
        soup = BeautifulSoup(output) 
        tags_gen = soup.recursiveChildGenerator()
        while True:
            try:
                tag = tags_gen.next()
                if not isinstance(tag, Tag):
                    continue
                if tag.has_key('dhash') and dhash not in tag['dhash'].split(' '): 
                    tag['dhash'] = tag['dhash'] + ' ' + dhash
                else:
                    tag['dhash'] = dhash
            except StopIteration:
                break
        return unicode(soup)
    
    tree = nice_inspect()
    #The only line from the original method - the rendering itself
    output = self.nodelist.render(context)
    return insert_metadata(tree, output)

if DTI_DEBUG:
    #Monkey-patching itself
    Template.__init__ = enhanced_init(Template.__init__)
    Template.render = render


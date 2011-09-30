from django.conf import settings
from django.template import Template, StringOrigin
from BeautifulSoup import BeautifulSoup, Tag
from hashlib import md5
import inspect, os
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

#Create a global variable that will be visible in modified template render 
#here we store all metadata about produced output
globals = local()

###Django template engine monkey-patching
#we enable meta-data collection in its runtime
trace_template = """<i>%(file)s</i><br/>
		    &nbsp;&nbsp;#%(line)s: %(func)s()<br/>
		    &nbsp;&nbsp;<small>%(code)s</small>"""

#Decorator over original init in order to store the template name
def enhanced_init(old_init):
    def new_init(self, template_string, origin=None, name='<Unknown Template>'):
        if origin is None:
            self.origin = StringOrigin(template_string)
        else:
            self.origin = origin
        return old_init(self, template_string, origin, name)
    return new_init

#New renderer method
def render(self, context):
    #print self.origin, self.name
    
    #Collect pathes to modules that have to be excluded from a trace tree: django & this module
    import django
    _exclude_path = (django.__file__.split('__init__')[0] , __file__.split('__init__')[0] )
    
    #Inspect the trace tree, collect usuful data
    tree = []
    frame = inspect.currentframe().f_back
    #skip excluded and only then gather few hops
    while frame.f_back and frame.f_code.co_filename.startswith(_exclude_path):
        frame = frame.f_back
    for i in range(1,3):
        if frame.f_code.co_filename.startswith(_exclude_path):
            frame = frame.f_back
            continue
        trace = inspect.getframeinfo(frame)
        filename = os.path.relpath(trace.filename, settings.SITE_BASEDIR )
        formatted = trace_template % { 'file': filename, 
                                       'line': trace.lineno, 
                                       'func': trace.function, 
                                       'code': "<br/>".join(trace.code_context)}
        tree.append( formatted.replace("'",'"') )
        frame = frame.f_back
 
    #add current rendering event to the global metadata with a hash
    info = {'origin': os.path.relpath(str(self.origin), settings.SITE_BASEDIR ), 
            #'name':   str(self.name),
            'tree': "<br/>".join(tree)}
    hash = md5(str(info['origin'])).hexdigest()
    globals.tdebug[hash] = info

    #The only line from the original method before patching - the rendering itself
    render = self.nodelist.render(context)
   
    #introduce a new attribute to each produced tag with a given hash or extend existing
    #WARNING: if produced HTML will be invalid, BeautifulSoup will try to fix it.
    soup = BeautifulSoup(render) 
    g = soup.recursiveChildGenerator()
    while True:
        try:
            tag = g.next()
            if not isinstance(tag, Tag):
                continue
            if tag.has_key('dhash') and hash not in tag['dhash'].split(' '): 
                tag['dhash'] = tag['dhash'] + ' ' + hash
            else:
                tag['dhash'] = hash
        except StopIteration:
            break    
    return unicode(soup)

#Monkey-patching itself
Template.__init__ = enhanced_init(Template.__init__)
Template.render = render


from django.conf import settings
from hashlib import md5
from BeautifulSoup import BeautifulSoup, Tag
from django.template import Template, StringOrigin
import inspect, os

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

globals = local()


def enhanced_init(old_init):
    def new_init(self, template_string, origin=None, name='<Unknown Template>'):
        if origin is None:
            self.origin = StringOrigin(template_string)
        else:
            self.origin = origin
        return old_init(self, template_string, origin, name)
    return new_init

def render(self, context):
    print self.origin, self.name
    import django
    _django_path = django.__file__.split('__init__')[0]
    _introspection_path = __file__.split('__init__')[0]
    #print _django_path, _introspection_path
    
    tree = []
    frame = inspect.currentframe().f_back
    while frame.f_back and ( frame.f_code.co_filename.startswith(_django_path) or frame.f_code.co_filename.startswith(_introspection_path) ):
        #print frame.f_code.co_filename
        frame = frame.f_back
    for i in range(1,3):
        if frame.f_code.co_filename.startswith(_django_path) or frame.f_code.co_filename.startswith(_introspection_path):
            frame = frame.f_back
            continue
        trace=inspect.getframeinfo(frame)
        filename = os.path.relpath(trace.filename, settings.SITE_BASEDIR )
        formatted = '<i>%s</i><br/>&nbsp;&nbsp;#%s: %s()<br/>&nbsp;&nbsp;<small>%s</small>' % (filename, trace.lineno, trace.function, "<br/>".join(trace.code_context))
        tree.append( formatted.replace("'",'"') )
        #tree.append(str(inspect.getframeinfo(frame)).replace("'",'"').replace(r"\n",""))
        frame = frame.f_back

    info = {'origin': os.path.relpath(str(self.origin), settings.SITE_BASEDIR ), 
            #'name':   str(self.name),
            'tree': "<br/>".join(tree)}

    hash = md5(str(info['origin'])).hexdigest()
    globals.tdebug[hash] = info

    render = self.nodelist.render(context)
    #return render
    soup = BeautifulSoup(render)
    g = soup.recursiveChildGenerator()
    while True:
        try:
            tag = g.next()
            if isinstance(tag, Tag):
                if tag.has_key('dhash'):
                    if hash not in tag['dhash'].split(' '): 
                        tag['dhash'] = tag['dhash'] + ' ' + hash
                else:
                    tag['dhash'] = hash
                #pass
        except StopIteration:
            break    
    return unicode(soup)
    #return '<span style="border: solid 1px red; display:block;">' + self.nodelist.render(context) + '</span>' + self.name #+'<!--'+ str(self.origin) +'-->'


Template.__init__ = enhanced_init(Template.__init__)
Template.render = render


from django.conf import settings
import os

if hasattr(settings, 'DTI_DEBUG'):
    DTI_DEBUG = settings.DTI_DEBUG
else:
    DTI_DEBUG = True

#These are not-logic values, can use 'and'-structure
#tempates of the bits that will be inserted into produced template
DTI_INSERT_FILES = hasattr(settings, 'DTI_INSERT_FILES') and settings.DTI_INSERT_FILES or \
                ('js/insertion.html',
                #'js/alertify.min.js',
                #'js/alertify.core.css',
                #'js/alertify.default.css',
                'js/jquery.jgrowl_minimized.js',
                'js/jquery.jgrowl.css')
DTI_PATH = hasattr(settings, 'DTI_PATH') and settings.DTI_PATH or \
           os.path.dirname(__file__)

#template of formating each trace chunk
DTI_TRACE_TEMPLATE = hasattr(settings, 'DTI_TRACE_TEMPLATE') and settings.DTI_TRACE_TEMPLATE or \
                    """<i>%(file)s</i><br/>
                    &nbsp;&nbsp;#%(line)s: %(func)s()<br/>
                    &nbsp;&nbsp;<small>%(code)s</small>"""

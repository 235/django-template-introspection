Django Template Introspection
=============================
  Did you ever had a web project which gave you hard times to find which bit of code generates the output?
  This project is developed with an idea *to help a developer in finding exact
  view(function) and template wich were used to generat every HTML tag in a resulting output*.

  And yes, it allows you to find the roots of all your content on a page visually in a browser:

  ![Screen sample](http://sumno.com.ua/media/images/galleries/2008/11/01/dlya-publikatsij/djangotemplateintrospection.png "Sample usage")


### Installation
  - Download the source, add drop `django_template_introspection` somewhere in the python path
  - Add `django_template_introspection` to the `INSTALLED_APPS` and `django_template_introspection.middleware.TemplateIntrospect` to the `MIDDLEWARE_CLASSES`.
For example, drop this to your `settings.py` somewhere to the very bottom (better to your `settings-local.py`):
    ```
      MIDDLEWARE_CLASSES += ('django_template_introspection.middleware.TemplateIntrospect',)
      INSTALLED_APPS += ('django_template_introspection',)
    ```
  - set `DTI_DEBUG = True`
  
Done! Next, you can:
  - Investigate the HTML output in your browser
  - Find out where each HTML tag was generated (its template & view function)

### Notes
  - Requires jQuery which is taken from a CDN, so it requires connection to Internet. Easy to fix
 

### TODO
 - clean-up js code (replace pop-up plugin?)
 - preserve the order of templates inclusion in the resulting output (is it a js problem?)
 - override the template-tag generator to mark template-tags in the inspection output also. They are processed during a template rendering and therefore are not currently highlighted. However, they are distinct chunks of code and have to be shown separately.

### Credits
 - using [jGrowl](http://stanlemon.net/projects/jgrowl.html) for nice pop-ups
 - using js code borrowed from [galambalazs](http://stackoverflow.com/questions/4711023/how-to-make-this-javascript-much-faster/4711224#4711224) for highliting and selecting HTML-elements
 - the idea of creating this module was offered by [askalyuk](https://github.com/askalyuk)

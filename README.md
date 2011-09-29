Django Template Introspection 
=============================
  Did you ever for a project where you cannot remember where exatly the all code is hidden? This project is developed with an idea *to help a developer in finding exactly wich view(function) using which template has generated every tempate tag in a resulting HTML output*.
  And yes, it allows you to find the roots of all content on a page visually in your browser:

  [Screen sample](http://sumno.com.ua/media/images/galleries/2008/11/01/dlya-publikatsij/menu015.png)
 
### Installation
 - Download sources, add place django_template_introspection somewhere in yours python path.
 - Add django_template_introspection to the INSTALLED_APPS and django_template_introspection.middleware.TemplateIntrospect to the MIDDLEWARE_CLASSES.
Django Template Introspection
=============================
  - Turn it on
  - Investigate the HTML output in your browser
  - Find out where each HTML tag was generated (its template & view)

  Did you ever had a project where you don't remember where exactly required code is hidden? This project is developed with an idea *to help a developer in finding exactly which view(function) and using which template has generated every HTML tag in a resulting output*.

  And yes, it allows you to find the roots of all content on a page visually in your browser:

  ![Screen sample](http://sumno.com.ua/media/images/galleries/2008/11/01/dlya-publikatsij/djangotemplateintrospection.png "Sample usage")

### Installation
 - Download the source, add place `django_template_introspection` somewhere in yours python path.
 - Add `django_template_introspection` to the `INSTALLED_APPS`.
 - Add `django_template_introspection.middleware.TemplateIntrospect` to the `MIDDLEWARE_CLASSES`.
 - Requires jQuery to be included. If you don't have it jet, add this to your base template after `<HEAD>` :

         <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">

### TODO
 - clean-up js code
 - preserve the order of templates inclusion in resulting output (is it a js problem?)
 - override the template-tag generator to mark template tags in the output also. They are processed in a single execution of the template renderer therefore are not currently highlighted. However, this is a distinct chunk of code and has to be showed separately.

### Credits
 - using [jGrowl](http://stanlemon.net/projects/jgrowl.html) for nice pop-ups
 - using js code borrowed from [galambalazs](http://stackoverflow.com/questions/4711023/how-to-make-this-javascript-much-faster/4711224#4711224) for highliting and selecting HTML-elements
 - the idea of creating this module was offered by [askalyuk](https://github.com/askalyuk)

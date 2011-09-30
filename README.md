Django Template Introspection
=============================
  - Turn on
  - Investigate HTML output in  your browser
  - find out where each HTML tag was generated (its template & view)

  Did you ever had a project where you don't remember where exactly required code is hidden? This project is developed with an idea *to help a developer in finding exactly which view(function) and using which template has generated every HTML tag in a resulting output*.
  And yes, it allows you to find the roots of all content on a page visually in your browser:

  ![Screen sample](http://sumno.com.ua/media/images/galleries/2008/11/01/dlya-publikatsij/menu015.png "Sample usage")

### Installation
 - Download the source, add place `django_template_introspection` somewhere in yours python path.
 - Add `django_template_introspection` to the `INSTALLED_APPS`
 - Add `django_template_introspection.middleware.TemplateIntrospect` to the `MIDDLEWARE_CLASSES`.
 - Requires jQuery to be included. If you don't have it jet, add this to your base template after `<HEAD>` :
         `<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">`

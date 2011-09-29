<style> 
  .outer { display:none; }
  .outer div { position:absolute; background:rgb(255,0,0); z-index:65000; }
</style> 

<script type="text/javascript">
jQuery(document).ready(function(){

/**
 * This object encapsulates the elements and actions of the overlay.
 * http://stackoverflow.com/questions/4711023/how-to-make-this-javascript-much-faster/4711224#4711224
 */
function Overlay(width, height, left, top) {
  
    this.width = this.height = this.left = this.top = 0;
  
    // outer parent
    var outer = jQuery("<div class='outer' />").appendTo("body");
    
    // red lines (boxes)
    var topbox    = jQuery("<div />").css("height", 1).appendTo(outer);
    var bottombox = jQuery("<div />").css("height", 1).appendTo(outer);  
    var leftbox   = jQuery("<div />").css("width",  1).appendTo(outer);
    var rightbox  = jQuery("<div />").css("width",  1).appendTo(outer);
  
    // don't count it as a real element
    outer.mouseover(function(){ 
        outer.hide(); 
    });
  
  
    /**
     * Public interface
     */
  
    this.resize = function resize(width, height, left, top) {
      if (width != null)
        this.width = width;
      if (height != null)
        this.height = height;
      if (left != null)
        this.left = left;
      if (top != null)
        this.top = top;      
    };
 
    this.show = function show() {
       outer.show();
    };
             
    this.hide = function hide() {
       outer.hide();
    };     

    this.render = function render(width, height, left, top) {
        
        this.resize(width, height, left, top);

        topbox.css({
          top:   this.top,
          left:  this.left,
          width: this.width
        });
        bottombox.css({
          top:   this.top + this.height - 1,
          left:  this.left,
          width: this.width
        });
        leftbox.css({
          top:    this.top, 
          left:   this.left, 
          height: this.height
        });
        rightbox.css({
          top:    this.top, 
          left:   this.left + this.width - 1, 
          height: this.height  
        });
          
        this.show();
    };      

    // initial rendering [optional]
    this.render(width, height, left, top);
}
  

// test
var box = new Overlay(2, 2, 5, 5);

var cspTimer;
function prepareChangeSearchParam(e, el) {
    if (cspTimer)
        clearTimeout(cspTimer);
    cspTimer = setTimeout(function() {
        $.jGrowl('close');

        el_dhash = el.attr('dhash');
        if (!el_dhash) {return;};
        hashes = el_dhash.split(' ');
        for ( var i=0, len=hashes.length; i<len; ++i ){
            $.jGrowl(dhash[hashes[i]].tree , 
                     { header: 'Template:'+dhash[hashes[i]].origin, 
                       sticky: true,
                       speed: 0,
		       animateOpen: { opacity: 'show' },
		       animateClose: { opacity: 'hide' },
                     });
        }
    }, 600);
}

jQuery("body").mouseover(function(e){
   var el = jQuery(e.target);
   var offset = el.offset();
   box.render(el.outerWidth(), el.outerHeight(), offset.left, offset.top);
   prepareChangeSearchParam(e, el);
});

});

</script>

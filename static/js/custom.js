(function ($, window, document, undefined) {
    'use strict';
    
    $(window).load(function () {
        // Animate loader off screen
        $('.se-pre-con').fadeOut('slow');
    });

    if ($.fn.navigation) {
        $("#navigation").navigation();
        $("#always-hidden-nav").navigation({
            hidden: true
        });
    }
    $(".always-btn-show").click(function () {
        $("#always-hidden-nav").data("navigation").toggleOffcanvas();
    });

    /* Sticky Header */
    var windows = $(window);
    $(window).on('scroll', function () {
        var scrollPos = $(this).scrollTop();
        if (scrollPos > 200) {
            $('.sticky-header,.sticky-mobile').addClass('is-sticky');
        } else {
            $('.sticky-header,.sticky-mobile').removeClass('is-sticky');
        }
    });
   

        /*============================================
     scrollUp
     ==============================================*/

    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    }); 
    
    

     function increment() {
        document.getElementById('qty2').stepUp();
    }
    function decrement() {
        document.getElementById('qty2').stepDown();
    }

    
    /*============================================
     quantity
     ==============================================*/ 


$(".qtyplus").click(function(){     
     $(this).parent().parent().find(":text[name='p_quantity']").val( Number($(this).parent().parent().find(":text[name='p_quantity']").val()) + 1 );
    });

$(".qtyminus").click(function(){
     if($(this).parent().parent().find(":text[name='p_quantity']").val()>1)
      $(this).parent().parent().find(":text[name='p_quantity']").val( Number($(this).parent().parent().find(":text[name='p_quantity']").val()) - 1 );

    }); 



                
})(jQuery, window, document);


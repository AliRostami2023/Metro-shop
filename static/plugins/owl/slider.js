(function () {
  "use strict";
  
  var carousels = function () {

    
    $(".lookbook-cat").owlCarousel({
      loop: false,
      margin: 30,
      responsiveClass: true,
      nav: false,
      autoplay:false,
      autoplayTimeout:5000,
      navigation:true,
       navText : ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
      responsive: {
        0: {
          items: 1,
          nav: false,
        },
        410: {
          items: 1,
          nav: false,
          loop: false,
        },
        680: {
          items: 2,
          nav: false,
          loop: false,
        },
         992: {
          items: 3,
          nav: false,
          loop: false
        },
        1200: {
          items: 3,
          nav: true,
        },
         1201: {
          items: 4,
           nav: true
        }
      }
    });
    
    $(".blog-slider").owlCarousel({
      loop: false,
      margin: 30,
      responsiveClass: true,
      nav: true,
      autoplay:false,
      autoplayTimeout:5000,
      navigation:true,
       navText : ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
      responsive: {
        0: {
          items: 1,
          nav: true
        },
        680: {
          items: 2,
          nav: true
        },
        992: {
          items: 2,
          nav: true
        },
        1200: {
          items: 3,
          nav: true
        }
      }
    });
    
       $(".brand-slider").owlCarousel({
      loop: true,
      margin: 30,
      responsiveClass: true,
      nav: false,
      autoplay:true,
      autoplayTimeout:3000,
      navigation:false,
       navText : false,
      responsive: {
        0: {
          items: 2
        },
        680: {
          items: 4
        },
        1000: {
          items: 7
        }
      }
    });
    
    
        $(".related").owlCarousel({
     loop: false,
      margin: 30,
      responsiveClass: true,
      nav: true,
      autoplay:false,
      autoplayTimeout:5000,
      navigation:true,
       navText : ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
     responsive: {
        0: {
          items: 1,
          nav: true
        },
        680: {
          items: 2,
          nav: true
        },
        992: {
          items: 3,
          nav: true
        },
        1200: {
          items: 5,
          nav: true
        }
      }
    });
    
    
    
    
   $(".special-product").owlCarousel({
      loop: false,
      margin: 10,
      responsiveClass: true,
      nav: false,
      autoplay:false,
      autoplayTimeout:3000,
      navigation:true,
      navText : false,
      responsive: {
        0: {
          items: 3,
          nav: true
        },
        680: {
          items: 4,
          nav: true,
        },
        1000: {
          items: 4,
          nav: true
        }
      }
    });
    
   $(".product-banner").owlCarousel({
      autoplay: true,
        autoplayTimeout: 4000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        autoplayHoverPause: true,
        smartSpeed: 700,
        loop: true,
        responsiveClass: true,
        items: 1,
        nav: false,
        navText: false,
        margin: 0,
        dots: false,
      responsive: {
        0: {
          items: 1,
          nav: true
        },
        680: {
          items: 1,
          nav: true,
        },
        1000: {
          items: 1,
          nav: true
        }
      }
    });

    
    $(".owl-slider").owlCarousel({
        autoplay: true,
        autoplayTimeout: 7000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        autoplayHoverPause: true,
        smartSpeed: 700,
        loop: true,
        responsiveClass: true,
        items: 1,
        nav: true,
        navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
        margin: 0,
        dots: false
    });

    $(".owl-slider").on('translate.owl.carousel', function () {
        $('.slider-item .img1.effect').removeClass('wow').hide();
        $('.slider-item .img2.effect').removeClass('wow').hide();
        $('.slider-item .slider-box .effect').removeClass('wow').hide();
    });

    $(".owl-slider").on('translated.owl.carousel', function () {
        $('.owl-item.active .slider-item .img1.effect').addClass('animated').show();
        $('.owl-item.active .slider-item .img2.effect').addClass('animated').show();
        $('.owl-item.active .slider-item .slider-box .effect').addClass('animated').show();
    });
    
    
    
 };
  (function ($) {
    carousels();
  })(jQuery);
})();



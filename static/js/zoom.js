	
			//Zoom Product
			$("#product-image2").elevateZoom({
        zoomType : "",
        cursor : "",
        easing: true,
         gallery: "thumbs2",
         galleryActiveClass: "active",
        loadingIcon : true
      });	
$("#product-image2").bind("click", function(e) {  
var ez =   $('#product-image2').data('elevateZoom');
ez.closeAll(); //NEW: This function force hides the lens, tint and window	
//$.fancybox(ez.getGalleryList());     
return false;
});

         
			//Zoom Product
			$("#product-image3").elevateZoom({
        zoomType : "",
        cursor : "",
        easing: true,
         gallery: "thumbs3",
         galleryActiveClass: "active",
        loadingIcon : true
      });	
$("#product-image3").bind("click", function(e) {  
var ez =   $('#product-image3').data('elevateZoom');
ez.closeAll(); //NEW: This function force hides the lens, tint and window	
//$.fancybox(ez.getGalleryList());     
return false;
});
        
        //Zoom Product
			$("#product-image").elevateZoom({
        zoomType : "inner",
        cursor : "crosshair",
        easing: true,
         gallery: "thumbs",
         galleryActiveClass: "active",
        loadingIcon : true,
        zoomWindowFadeIn: 300,
        zoomWindowFadeOut: 300
      });	
$("#product-image").bind("click", function(e) {  
var ez =   $('#product-image').data('elevateZoom');
ez.closeAll(); //NEW: This function force hides the lens, tint and window	
//$.fancybox(ez.getGalleryList());     
return false;
});

         
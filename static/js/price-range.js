(function ($, window, document, undefined) {
    'use strict';

			$('#slider-range').slider({
				range: true,
				min: 0,
				max: 500,
				values: [0, 400],
				slide: function (event, ui) {
					$('#amount').text('$' + ui.values[0] + ' - $' + ui.values[1]);
				}
			});
			$('#amount').text('$' + $('#slider-range').slider('values', 0) + ' - $' + $('#slider-range').slider('values', 1));



		


                
})(jQuery, window, document);


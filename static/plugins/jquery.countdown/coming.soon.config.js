$(function () {
	var austDay = new Date();
	austDay = new Date(austDay.getFullYear() + 1, 22 - 08, 22);
	$('.countdown').countdown({until: austDay});
	$('#year').text(austDay.getFullYear());
        
        austDay = new Date(austDay.getFullYear() + 1, 0 - 2, 0);
	$('.countdown2').countdown({until: austDay});
	$('#year').text(austDay.getFullYear());
});
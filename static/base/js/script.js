$(document).ready(function() {

	$(".nav-toggle-label").click(function() {
		var element = document.getElementById("nav-toggle");

		if (element.checked != true) {
			$("nav").addClass("nav-clicked");
		} else {
			window.setTimeout(function(){
				$("nav").removeClass("nav-clicked");
			}, 500);
		}
	});

	$(document).click(function(evt) {
		if (!$(evt.target).is('#nav-toggle') && !$(evt.target).is('span') && !$(evt.target).is('#nav-toggle-label') && !$(evt.target).is('nav a')) {
	    	$('#nav-toggle').prop('checked', false);
	    	window.setTimeout(function(){
				$("nav").removeClass("nav-clicked");
			}, 500);
		}
	});


	//CLOSE DJANGO MESSAGES

	$(".content-container").on("click", ".close-messages", function() {
		$(this).parent().hide(700);
		return false;
	});

	if ($(".messages").length) {
		window.setTimeout(function(){
			$(".messages").hide(700);
		}, 5000);
	}
	
});
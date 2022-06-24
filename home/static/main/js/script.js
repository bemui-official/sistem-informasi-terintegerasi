$(document).ready(function() {

	//NAVBAR FIXED

	var headerHeigth = $("header").height();

	$(window).scroll(function() {
		if (document.getElementById("nav-toggle").checked != true) {
			if ($(this).scrollTop() > 40) {
				$("header").removeClass("header-transparent");
				$("header").addClass("header-white");
			} else {
				$("header").removeClass("header-white");
				$("header").addClass("header-transparent");
			}
		}
	});

	//header white when toggle checked

	$(".nav-toggle-label").click(function() {
		var element = document.getElementById("nav-toggle");

		if (element.checked != true) {
			$("header").removeClass("header-transparent");
			$("header").addClass("header-white");
		} else if ($(window).scrollTop() < 40) {
			window.setTimeout(function(){
				$("header").removeClass("header-white");
				$("header").addClass("header-transparent");
			}, 300);
		}
	});

	$(document).click(function(evt) {
		if (!$(evt.target).is('#nav-toggle') && !$(evt.target).is('span') && !$(evt.target).is('#nav-toggle-label') && !$(evt.target).is('nav a')) {
	    	window.setTimeout(function(){
				if ($(window).scrollTop() < 40) {
					$("header").removeClass("header-white");
					$("header").addClass("header-transparent");
				}
			}, 300);
		}
	});


});
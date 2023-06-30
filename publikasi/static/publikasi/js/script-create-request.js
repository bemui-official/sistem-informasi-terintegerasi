$(document).ready(function() {

	//loading

	var loadingBackground = $("#loading-background");

	$('#button-submit').on('click', function() {
		var publikasURL = $("input[name='publikas']").val();
		var buktiInsidentalURL = $("input[name='bukti_insidental']").val();
		if (validURL(publikasURL) && (buktiInsidentalURL == "" || validURL(buktiInsidentalURL))) {
			loadingBackground.css('display', 'flex');
		}
	});

	function validURL(str) {
		var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
		'((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
		'((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
		'(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
		'(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
		'(\\#[-a-z\\d_]*)?$','i'); // fragment locator
		return !!pattern.test(str);
	}

	//form

	checkIsInsidental();

	document.getElementById("button-submit").disabled = true;
	$("#button-submit").addClass("button-disabled");

	window.setTimeout(function() {
    	checkIsFormFilledCreateRequest();
    }, 200);

	$('#radio-is-insidental-0, #radio-is-insidental-1').on('click', function() {
		window.setTimeout(function() {
			checkIsInsidental();
		}, 20);
	});

	function checkIsInsidental() {
		var target = document.getElementById('id_is_insidental_0').checked;
		if (target) {
			$("form-label-bukti-insidental").show();
			$("#bukti-insidental").show();
		} else {
			$("form-label-bukti-insidental").hide();
			$("#bukti-insidental").hide();
			$("#id_bukti_insidental").val('');
		}
	}


	$("input[type='url'], input[type='text']").on("keyup input change", function(){
	    checkIsFormFilledCreateRequest();
	});

	$('#radio-is-insidental-0, #radio-is-insidental-1').on('click', function() {
		window.setTimeout(function() {
	    	checkIsFormFilledCreateRequest();
	    }, 20);
	});


	function checkIsFormFilledCreateRequest() {
		if ($("input[name='program']").val() != "" && $("input[name='publikas']").val() != "") {
	        
	        var target = document.getElementById('id_is_insidental_0').checked;

	        if (!target) {
	        	document.getElementById("button-submit").disabled = false;
	        	$("#button-submit").removeClass("button-disabled");
	    	} else {
	    		if ($("input[name='bukti_insidental']").val() != "") {
	    			document.getElementById("button-submit").disabled = false;
	        		$("#button-submit").removeClass("button-disabled");
	    		} else {
	    			document.getElementById("button-submit").disabled = true;
	    			$("#button-submit").addClass("button-disabled");
	    		}
	    	}
	    } else {
	        document.getElementById("button-submit").disabled = true;
	    	$("#button-submit").addClass("button-disabled");
	    }
	}


	var time_available = {"09:00" : "09:00", "10:00" : "10:00", "12:00" : "12:00", "13:00" : "13:00", "14:00" : "14:00", "15:00" : "15:00", "16:00" : "16:00", "17:00" : "17:00", "18:00" : "18:00", "19:00" : "19:00", "20:00" : "20:00"};

	removeTakenTime($("input[type='date']").val());
	$("input[type='date']").change(function() {
		var date = $(this).val();
	    checkTimeAvailable(date);
	});

	function checkTimeAvailable(date) {
	    document.getElementById("time_posted_form").options.length = 0;

	    var select = $('#time_posted_form')
    	$.each(time_available, function(key, value) {   
		     select.append($("<option></option>")
		                    .attr("value", key)
		                    .text(value)); 
		});

    	removeTakenTime(date);
    	if (self_time != "" && $("#time_posted_form option[value='" + self_time + "']").length > 0) {
    		select.val(self_time);
    	}
	}

	function removeTakenTime(date) {
		for (const [key, value] of Object.entries(time_taken_dict)) {
		  	if (key == date) {
		  		for (const [time_key, time_value] of Object.entries(value)) {
		  			if (time_value != self_time || key != self_date) {
		  				$("#time_posted_form option[value='" + time_value + "']").remove();
		  			}
			  	}
			}
		}
	}

});
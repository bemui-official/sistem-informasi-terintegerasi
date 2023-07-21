$(document).ready(function() {

	var modalHapus = document.getElementById("modal-hapus");
	var modalTerima = document.getElementById("modal-terima");
	var modalTolak = document.getElementById("modal-tolak");
	var modalSelesai = document.getElementById("modal-selesai");

	var btnHapus = document.getElementById("delete-request");
	var btnTerima = document.getElementById("button-terima");
	var btnTolak = document.getElementById("button-tolak");
	var btnSelesai = document.getElementById("button-selesai");

	var closeHapus1 = document.getElementById("close-hapus1");
	var closeHapus2 = document.getElementById("close-hapus2");
	var closeTerima1 = document.getElementById("close-terima1");
	var closeTerima2 = document.getElementById("close-terima2");
	var closeTolak1 = document.getElementById("close-tolak1");
	var closeTolak2 = document.getElementById("close-tolak2");
	var closeSelesai1 = document.getElementById("close-selesai1");
	var closeSelesai2 = document.getElementById("close-selesai2");

	// hapus
	if (modalHapus != null && btnHapus != null && closeHapus1 != null && closeHapus2 != null) {
		// open the modal on click 
		btnHapus.onclick = function() {
			modalHapus.style.display = "flex";
		}

		// close the modal
		closeHapus1.onclick = function() {
			modalHapus.style.display = "none";
		}

		closeHapus2.onclick = function() {
			modalHapus.style.display = "none";
		}
	}


	// terima
	if (modalTerima != null && btnTerima != null && closeTerima1 != null && closeTerima2 != null) {
		btnTerima.onclick = function() {
			modalTerima.style.display = "flex";
		}

		closeTerima1.onclick = function() {
			modalTerima.style.display = "none";
		}

		closeTerima2.onclick = function() {
			modalTerima.style.display = "none";
		}
	}

	// tolak
	if (modalTolak != null && btnTolak != null && closeTolak1 != null && closeTolak2 != null) {
		btnTolak.onclick = function() {
			modalTolak.style.display = "flex";
		}

		closeTolak1.onclick = function() {
			modalTolak.style.display = "none";
		}

		closeTolak2.onclick = function() {
			modalTolak.style.display = "none";
		}
	}

	// selesai
	if (modalSelesai != null && btnSelesai != null && closeSelesai1 != null && closeSelesai2 != null) {
		btnSelesai.onclick = function() {
			modalSelesai.style.display = "flex";
		}

		closeSelesai1.onclick = function() {
			modalSelesai.style.display = "none";
		}

		closeSelesai2.onclick = function() {
			modalSelesai.style.display = "none";
		}
	}

	window.onclick = function(event) {
		if (event.target == modalHapus || event.target == modalTerima || event.target == modalTolak || event.target == modalSelesai) {
	  		if (modalHapus != null) {
	  			modalHapus.style.display = "none";
	  		}
	  		if (modalTerima != null) {
	  			modalTerima.style.display = "none";
	  		}
	  		if (modalTolak != null) {
	  			modalTolak.style.display = "none";
	  		}
	  		if (modalSelesai != null) {
	  			modalSelesai.style.display = "none";
	  		}
		}
	}

	//loading

	var loadingBackground = $("#loading-background");

	$('#button-terima-real, #button-tolak-real, #button-selesai-real').on('click', function() {
		if (modalHapus != null) {
  			modalHapus.style.display = "none";
  		}
  		if (modalTerima != null) {
  			modalTerima.style.display = "none";
  		}
  		if (modalTolak != null) {
  			modalTolak.style.display = "none";
  		}
  		if (modalSelesai != null) {
  			modalSelesai.style.display = "none";
  		}

  		var designLink = $("input[name='design_link']").val();
  		var previewIGLink = $("input[name='preview_link_instagram']").val();
  		var previewTwitterLink = $("input[name='preview_link_twitter']").val();
  		if (designLink != null) {
  			if (designLink == "" || validURL(designLink)) {
  				loadingBackground.css('display', 'flex');
  			}
  		} else if (previewIGLink != null || previewTwitterLink != null) {
  			if ((previewIGLink == "" || validURL(previewIGLink)) && (previewTwitterLink == "" || validURL(previewTwitterLink))) {
  				loadingBackground.css('display', 'flex');
  			}
  		} else {
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

	//kembali

	$("#button-kembali").on("click", function() {
		window.close();
	});
});
// Get the modal
var modal = document.getElementsByClassName("modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementsByClassName("bukti-image");
var modalImg = document.getElementsByClassName("modal-content");
img.onclick = function(){
  console.log("masuk")
  modal.style.display = "block";
  modalImg.src = this.src;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}
// -------------
// FUNGSI MODAL
// -------------
var modal = document.getElementsByClassName("modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementsByClassName("bukti-image");
var modalImg = document.getElementsByClassName("modal-content");

console.log(img)

function modalFunction() {
  console.log(modal)
  console.log(modalImg)
  modal[0].style.display = "block";
  modalImg[0].src = this.src;
}

function spanFunction() {
  console.log("masuk2")
  modal[0].style.display = "none";
}

for (var i = 0 ; i < img.length; i++) {
   img[i].addEventListener('click' , modalFunction) ;
   modal[i].addEventListener('click', spanFunction)
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close");
for (var i = 0 ; i < span.length; i++) {
   span[i].addEventListener('click' , spanFunction) ;
}

// -------------
// Currency Converter
// -------------
let x = document.querySelectorAll(".currency");
for (let i = 0, len = x.length; i < len; i++) {
    let num = Number(x[i].innerHTML)
              .toLocaleString('en');
    x[i].innerHTML = num;
    x[i].classList.add("currSign");
}

// -------------
// Delete Modal
// -------------
var modal = document.getElementById('modal_del');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
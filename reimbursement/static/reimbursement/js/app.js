/**
 *
 * app.js
 *
 */

// function readFile(input) {
//      if (input.files && input.files[0]) {
//          filess = input.files
//          var reader = new FileReader();
//          const fileArray = [...filess];
//
//          reader.onload = function (e) {
//              var htmlPreview =
//                  '<img width="100" src="' + e.target.result + '" />'+
//                  '<p>' + input.files[0].name + '</p>';
//              var wrapperZone = $(input).parent();
//              var previewZone = $(input).parent().parent().find('.preview-zone');
//              var boxZone = $(input).parent().parent().find('.preview-zone').find('.box').find('.box-body');
//
//              wrapperZone.removeClass('dragover');
//              previewZone.removeClass('hidden');
//              // boxZone.empty();
//              boxZone.append(htmlPreview);
//          };
//
//          for (let i = 0; i < fileArray.length; i++){
//                   reader.readAsDataURL(input.files[0]);
//          }
//      }
// }
// function reset(e) {
//     e.wrap('<form>').closest('form').get(0).reset();
//     e.unwrap();
// }
//
// $(".dropzone").change(function(){
//     e.preventDefault();
//     e.stopPropagation();
//     readFile(this);
// });
// $('.dropzone-wrapper').on('dragover', function(e) {
//     $(this).addClass('dragover');
// });
// $('.dropzone-wrapper').on('dragleave', function(e) {
//     e.preventDefault();
//     e.stopPropagation();
//     $(this).removeClass('dragover');
// });
// $('.remove-preview').on('click', function() {
//     var boxZone = $(this).parents('.preview-zone').find('.box-body');
//     var previewZone = $(this).parents('.preview-zone');
//     var dropzone = $(this).parents('.form-group').find('.dropzone');
//     boxZone.empty();
//     previewZone.addClass('hidden');
//     reset(dropzone);
// });

// const initApp = () => {
//     const droparea = document.querySelector('.dropzone-wrapper');
//
//     const active = () => droparea.classList.add("dark-bg");
//
//     const inactive = () => droparea.classList.remove("dark-bg");
//
//     const prevents = (e) => e.preventDefault();
//
//     ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
//         droparea.addEventListener(evtName, prevents);
//     });
//
//     ['dragenter', 'dragover'].forEach(evtName => {
//         droparea.addEventListener(evtName, active);
//     });
//
//     ['dragleave', 'drop'].forEach(evtName => {
//         droparea.addEventListener(evtName, inactive);
//     });
//
//     droparea.addEventListener("drop", handleDrop);
//
// }
//
// document.addEventListener("DOMContentLoaded", initApp);
//
// const handleDrop = (e) => {
//     const dt = e.dataTransfer;
//     const files = dt.files;
//     const fileArray = [...files];
//     console.log(files); // FileList
//     console.log(fileArray);
//
// }

Dropzone.options.uploadForm = { // The camelized version of the ID of the form element

  // The configuration we've talked about above
  autoProcessQueue: false,
  uploadMultiple: true,
  parallelUploads: 100,
  maxFiles: 100,

  // The setting up of the dropzone
  init: function() {
    var myDropzone = this;

    // First change the button to actually tell Dropzone to process the queue.
    this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();
      myDropzone.processQueue();
    });

    // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
    // of the sending event because uploadMultiple is set to true.
    this.on("sendingmultiple", function() {
      // Gets triggered when the form is actually being sent.
      // Hide the success button or the complete form.
    });
    this.on("successmultiple", function(files, response) {
      // Gets triggered when the files have successfully been sent.
      // Redirect user or notify of success.
    });
    this.on("errormultiple", function(files, response) {
      // Gets triggered when there was an error sending the files.
      // Maybe show form again, and notify user of error
    });
  }

}
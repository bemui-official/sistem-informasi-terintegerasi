

// -----------------
// UUID4 Function
// -----------------
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16));
}


// -----------------
// Javascript Event Handler
// -----------------
document.getElementById("submitbutton").addEventListener("click", function() {
    console.log("Submit Button")
    uppy.upload()
})


// ---------------
// Uppy Settings
// ---------------
uppy.use(Uppy.XHRUpload, {
    endpoint: '../backend/upload_photo',
    headers: {'X-CSRFToken':csrftoken},
    formData: true,
    fieldName: 'file'
})
uppy.use(Uppy.Dashboard, {
    inline: true,
    target: '#drag-drop-area',
    proudlyDisplayPoweredByUppy:false,
    showProgressDetails:true,
    doneButtonHandler: null,
    hideUploadButton: true,
})
uppy.on('complete', (result) => {
    console.log('Upload complete! We’ve uploaded these files:', result.successful)
})
uppy.use(Uppy.Form, {
    target: "#form",
    resultName: 'uploadFiles',
    getMetaFromForm: false,
    addResultToForm: true,
    submitOnSuccess: true,
    triggerUploadOnSubmit: false,
})
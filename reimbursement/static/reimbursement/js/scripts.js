
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
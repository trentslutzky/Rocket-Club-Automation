function copy_to_cb() {
  /* Get the text field */
  var copyText = document.getElementById("attendance-input");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");
  copyText.deselect();
} 
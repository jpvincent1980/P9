// Handles the appearance/disappearance of the password
function ShowPassword(pass) {
var password = document.getElementById(pass);
if (password.type === "password") {
password.type = "text";
} else {
password.type = "password"}
}

// Handles the appearance and disappearance of a Back To Top button at the
// bottom right of the screen
const backToTopButton = document.getElementById("backToTop");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    backToTopButton.style.opacity = 1;
  } else {
    backToTopButton.style.opacity = 0;
  }
}
function backToTopFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
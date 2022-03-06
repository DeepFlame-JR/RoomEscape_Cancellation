console.log('Client-side code running');

const button = document.getElementById('registerButton');
const email_element = document.getElementById('email');
const theme_element = document.getElementById('theme');

button.addEventListener('click', function(e) {
  alert("test")
  var email = email_element.value;
  var theme = theme_element.value;
  var msg = "아래 정보가 맞습니까?\nE-mail: " + email + "\n테마: " + theme
  alert(msg)
  // console.log('button was clicked');
});

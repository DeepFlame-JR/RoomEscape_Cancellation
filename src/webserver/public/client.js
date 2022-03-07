// require packages
const button = document.getElementById('registerButton');
const email_element = document.getElementById('email');
const theme_element = document.getElementById('theme');


button.addEventListener('click', function(e) {
  var email = email_element.value;
  var select = theme_element.value;
  var arr = select.split("|");
  var cafe = arr[0].trim();
  var theme = arr[1].trim();

  var msg = "아래 정보가 맞습니까?\nE-mail: " + email + "\n카페: " + cafe + "\n테마: " + theme;
  var result = confirm(msg);

  if(result){
    fetch('/clicked', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        cafe: cafe,
        theme: theme,
      })
    })
    .then(function(res){
      if(res.ok){
        alert('click was recorded');
        return res.json();
      }
    })
    .catch((err) => console.log(err));
  }
});

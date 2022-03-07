// require packages
const registerButton = document.getElementById('registerButton');
const deleteButton = document.getElementById('deleteButton');
const email_element = document.getElementById('email');
const theme_element = document.getElementById('theme');

function getUserInfo(){
  var email = email_element.value;
  var select = theme_element.value;
  var arr = select.split("|");
  var cafe = arr[0].trim();
  var theme = arr[1].trim();

  if(email.includes('@') == false){
    alert("E-mail을 확인해주세요.");
    return null;
  }

  var userInfo = {
    email: email,
    cafe: cafe,
    theme: theme,
  };
  return userInfo;
}

registerButton.addEventListener('click', function(e) {
  var userInfo = getUserInfo();
  if(userInfo == null) return;

  // register
  var msg = "아래 정보를 등록합니다.\nE-mail: " + userInfo.email +
            "\n카페: " + userInfo.cafe +
            "\n테마: " + userInfo.theme;
  var result = confirm(msg);

  if(result){
    fetch('/clicked', {
      method: 'POST',
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify(userInfo)
    })
    .then(function(res){
      if(res.ok){
        alert('등록이 완료되었습니다!');
      }else{
        alert('위 정보가 이미 존재합니다.');
      }
    })
    .catch((err) => console.log(err));
  }
});

deleteButton.addEventListener('click', function(e) {
  var userInfo = getUserInfo();
  if(userInfo == null) return;

  // delete
  var msg = "아래 정보를 삭제합니다.\nE-mail: " + userInfo.email +
            "\n카페: " + userInfo.cafe +
            "\n테마: " + userInfo.theme;
  var result = confirm(msg);

  if(result){
    fetch('/deleted', {
      method: 'POST',
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify(userInfo)})
      .then(function(res){
        if(res.ok){
          alert('제거되었습니다.');
        }else{
          alert('등록된 정보가 없습니다.');
        }
      })
      .catch((err) => console.log(err));
  }
});

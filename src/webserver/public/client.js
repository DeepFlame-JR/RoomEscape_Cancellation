// require packages
const registerButton = document.getElementById('registerButton');
const deleteButton = document.getElementById('deleteButton');
const email_element = document.getElementById('email');
const theme_element = document.getElementById('theme');
const untilMonth_element = document.getElementById('untilMonth');

function getUserInfo(){
  var email = email_element.value;
  var select = theme_element.value;
  var arr = select.split("|");
  var cafe = arr[0].trim();
  var theme = arr[1].trim();
  var untilMonth = untilMonth_element.value;

  if(email.includes('@') == false){
    alert("E-mail을 확인해주세요.");
    return null;
  }

  var userInfo = {
    email: email,
    cafe: cafe,
    theme: theme,
    untilMonth: untilMonth
  };
  return userInfo;
}

function stringifyInfo(dict, isRegister){
  msg = "E-mail: " + dict.email +
          "\n카페: " + dict.cafe +
          "\n테마: " + dict.theme;
  if(isRegister)
    msg = msg + "\n알림받을 최근 개월 수: " + dict.untilMonth;

  return msg;
}

registerButton.addEventListener('click', function(e) {
  var userInfo = getUserInfo();
  if(userInfo == null) return;

  // register
  var msg = "아래 정보를 등록합니다.\n" + stringifyInfo(userInfo, true);
  var result = confirm(msg);

  if(result){
    fetch('/register', {
      method: 'POST',
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify(userInfo)
    })
    .then(function(res){
      if(res.ok){
        alert('등록이 완료되었습니다!');
      }
      else if(res.status == 404){
        alert("이미 등록된 유저 정보가 있습니다.\n알림받을 최근 개월 수를 변경했습니다.");
      }
    })
    .catch(function(err){
      console.log(err);
    });
  }
});

deleteButton.addEventListener('click', function(e) {
  var userInfo = getUserInfo();
  if(userInfo == null) return;

  // delete
  var msg = "아래 정보를 제거합니다.\n" + stringifyInfo(userInfo, false);
  var result = confirm(msg);

  if(result){
    fetch('/delete', {
      method: 'POST',
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify(userInfo)})
      .then(function(res){
        if(res.ok){
          alert('제거되었습니다.');
        }else if(res.status == 404){
          alert('등록된 정보가 없습니다.');
        }
      })
      .catch((err) => console.log(err));
  }
});

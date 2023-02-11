function signup() {
  const id = document.querySelector('#signup_box_id').value;
  const pw = document.querySelector('#signup_box_pw1').value;
  const pw_doubleCheck = document.querySelector('#signup_box_pw2').value;
  const nick = document.querySelector('#signup_box_nickName').value;

  // 비밀번호 검증 필요
  if (pw !== pw_doubleCheck) {
    alert('비밀번호 중복');
    return;
  }

  $.ajax({
    type: 'POST',
    url: '/account/signup',
    data: {
      user_id: id,
      user_password: pw,
      user_nickname: nick,
    },
    success: function (response) {
      alert(response['msg']);
      window.close();
    },
  });
}

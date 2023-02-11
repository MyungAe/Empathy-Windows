// let login = document.querySelector("#login")

$(document).ready(() => {
  const nickname = localStorage.getItem('nickname');
  if (nickname) {
    const signin = document.querySelector('.sign');
    signin.innerText = `${nickname} 님 | 로그아웃`;
    return;
  }

  if (!nickname) {
    const signin = document.querySelector('.sign');
    signin.innerText = `로그인`;
    return;
  }
});

function login_signup() {
  let top = (screen.height - 300) / 2;
  let left = (screen.width - 300) / 2;
  window.open(
    '/account/',
    'open',
    'width=500, height=300, top =' + top + ', left=' + left
  );
}

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
      user_password: pw1,
      user_nickname: nick,
    },
    success: function (response) {
      alert(response['msg']);
    },
  });
}

function signin() {
  const signin = document.querySelector('.sign').innerText;

  if (signin == '로그인') {
    const id = document.querySelector('#login_box_id').value;
    const pw = document.querySelector('#login_box_pw').value;

    $.ajax({
      type: 'POST',
      url: '/account/signin',
      data: {
        user_id: id,
        user_password: pw,
      },
      success: function (response) {
        alert(response['msg']);
        localStorage.setItem('accessToken', response.access_token);
        localStorage.setItem('nickname', response.user_nickname);
        window.location.reload();
      },
    });
  }

  if (signin != '로그인') {
    localStorage.clear();
  }
}

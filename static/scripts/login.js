// input[id='login_sidebar']:checked + label + div {
//   right: 0;
// }

$(document).ready(() => {
  // const input = document.querySelector

  const nickname = localStorage.getItem('nickname');
  const signin = document.querySelector('.sign');

  if (nickname) {
    signin.innerText = `${nickname}님`;

    const logout_tag = `<li style="margin-left: 10px;">
                          <a
                            href="#"
                            id="mideoArea"
                            onclick="signout()"
                          >
                            로그아웃
                          </a>
                        </li>`;

    $('#navibar').append(logout_tag);
    return;
  }
  if (!nickname) {
    signin.innerText = `로그인`;
    return;
  }
});

function isSign() {
  const username = localStorage.getItem('nickname');

  if (!username) {
    // checkbox = True : 사이드바 나와야됨
    return true;
  } else {
    // checkbox = False : 사이드바 안나와야됨
    return false;
  }
}

function signout() {
  localStorage.clear();
  window.location.reload();
}

function login_signup() {
  let top = (screen.height - 300) / 2;
  let left = (screen.width - 300) / 2;
  window.open(
    '/account/',
    'open',
    'width=500, height=300, top =' + top + ', left=' + left
  );
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

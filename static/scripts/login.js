// let login = document.querySelector("#login")
function login_singup() {
  let top = (screen.height-300)/2;
      let left = (screen.width-500)/2;
      window.open('/account/signup2', 'open', 'width=500, height=300, top ='+top+', left='+left);
}

function login() {
    let id = document.querySelector('#login_box_id').value
    let pw = document.querySelector('#login_box_pw').value
    
    if(id === "" || pw === "") {
      alert("아이디 또는 비밀번호가 입력되지 않았습니다.")
      return
    } else {
      $.ajax({
        type:"POST",
        url:"/account/signin2",
        data:{"id_give":id, "pw_give":pw},
        success: function(response) {
          alert(response['msg'])
        }
      })
    }
    document.querySelector('#login_sidebar').checked = false;
      
}

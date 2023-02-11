// let login = document.querySelector("#login")
function login_singup() {
  let top = (screen.height-300)/2;
      let left = (screen.width-300)/2;
      window.open('/account/signup2', 'open', 'width=500, height=300, top ='+top+', left='+left);
}


function signup() {
  let id = document.querySelector('#signup_box_id').value
  let pw1 = document.querySelector('#signup_box_pw1').value
  let pw2 = document.querySelector('#signup_box_pw2').value
  let nick = document.querySelector('#signup_box_nickName').value
  console.log(id, pw1,pw2,nick)  

  $.ajax({
    type:"POST",
    url:"/account/signup2check",
    data:{'id_give':id,'pw_give':pw1,'nick_give':nick},
    success:function(response) {
      alert(response['msg'])
    }
  })
}

function login() {
    let id = document.querySelector('#login_box_id').value
    let pw = document.querySelector('#login_box_pw').value
    
    $.ajax({
      type:"POST",
      url:"/account/signin2",
      data:{"id_give":id, "pw_give":pw},
      success: function(response) {
        alert(response['msg'])
      }
    })

}

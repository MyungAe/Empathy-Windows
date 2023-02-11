function signup() {
  let id = document.querySelector('#signup_box_id').value
  let pw1 = document.querySelector('#signup_box_pw1').value
  let pw2 = document.querySelector('#signup_box_pw2').value
  let nick = document.querySelector('#signup_box_nickName').value
  
  if(pw1 === pw2) {
    $.ajax({
      type:"POST",
      url:"/account/signup2check",
      data:{'id_give':id,'pw_give':pw1,'nick_give':nick},
      success:function(response) {
        alert(response['msg'])
        window.close()
      }
    })
  } else {
    alert("비밀번호가 일치하지 않습니다.")
  }


}
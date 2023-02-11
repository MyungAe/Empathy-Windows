//댓글 저장

//댓글 수정
function commentPatch() {
    let update = prompt('수정사항을 입력해주세요.')
    alert(update)
    $.ajax({
        type: "FATCH",
        url: "/music/comment/",
        data: {comment_give: update},
        success: function (response) {
            console.log(response["msg"])
        }
    });
}

//댓글 삭제
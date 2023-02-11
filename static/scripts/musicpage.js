//get music data
$(document).ready(function () {
    show_music();
    show_comment();
});

function show_music() {
    $.ajax({
        type: "GET",
        url: "/music",
        data: {},
        success: function (response) {
            console.log(response["music"])

            let rows = response["music"]
            for (let i=0; i<rows.length; i++){
                let rank = rows[i]['rank']
                let singer = rows[i]['singer']
                let title = rows[i]['title']

                let temp_html = `<div class="container">
                                  <div class="row">
                                    <div class="col">
                                      ${rank}
                                    </div>
                                    <div class="col">
                                      ${singer}
                                    </div>
                                    <div class="col">
                                      ${title}
                                    </div>
                                  </div>
                                </div>`
                $('#musicListData').append(temp_html)
            }
        }
    });
}

//댓글 저장
function save_comment() {
    let comment = $('#comment').val()

    //날짜 코드
    let today = new Date();
    let year = String(today.getFullYear());
    let mon = (('0' + (today.getMonth() + 1)).slice(-2));
    let date = ('0' + (today.getDate())).slice(-2);
    let fullDate = `${year}-${mon}-${date}`

    $.ajax({
        type: "POST",
        url: "/music/comment",
        data: {comment_give: comment, date_give: fullDate},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

//댓글 보기
function show_comment() {
    $.ajax({
        type: "GET",
        url: "/music/comment",
        data: {},
        success: function (response) {
            console.log(response)
            let rows = response['comments']
            for (let i = 0; i < rows.length; i++) {
                let nickname = rows[i]['nickname']
                let num = rows[i]['num']
                let comment = rows[i]['comment']
                let date = rows[i]['date']

                let temp_html = `<div id="commentcard">
                                    <div class="card-header">
                                        <p>${date}</p>


                                         <div class="card-header-btns">
                                            <button onclick="commentPatch(${num})" class="btn btn-outline-success">수정하기</button>
                                            <button onclick="del_comment(${num})" class="btn btn-outline-danger">삭제하기</button>
                                        </div>

                                    </div>
                                    <div id="card-body">
                                        <blockquote class="blockquote mb-0">
                                            <p>${num}- ${comment}</p>
                                            <footer class="blockquote-footer" style="color: white">${nickname}</cite>
                                            </footer>
                                            <div id="card-header-btns">
                                                <button onclick="commentPatch()">수정하기</button>
                                                <button onclick="del_comment(${num})">삭제하기</button>
                                            </div>
                                        </blockquote>
                                    </div>
                                </div>`
                $('#comment-list').append(temp_html)
            }
        }
    });
}






//댓글 수정
function commentPatch(num) {
    let update = prompt('수정사항을 입력해주세요.')
    console.log(num)
    $.ajax({
        type: "PATCH",
        url: "/music/comment",
        data: {comment_give: update, num_give : num},
        success: function (response) {
            console.log(response["msg"])
            window.location.reload()
        }
    });
}

//댓글 삭제
function del_comment(num) {
    $.ajax({
        type: 'DELETE',
        url: '/music/comment',
        data: {num_give: num},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}
//get music data
$(document).ready(function () {
    show_music();
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

                let temp_html = `<div id="musicHtml">
                                    <div>${rank}</div>
                                    <div>${singer}</div>
                                    <div>${title}</div>
                                </div>`
                $('#musicListData').append(temp_html)
            }
        }
    });
}

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
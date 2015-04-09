
function open_comment_form(id, path){
    var csrftoken = $.cookie('csrftoken');
    var div = $("#comment"+id);
    div.append("<form action='"+path+"'method='POST'/>");
    var post = $("#comment"+id+" form");
    post.append("<input type='hidden' name='csrfmiddlewaretoken' value='"+csrftoken+"'>");
    post.append("<input type='text' placeholder='Нет ничего лучше хорошего комментария' name='comment-text'/>");
    post.append("<br><input type='submit' value = 'Комментировать' />");
    post.append("</form>");
}

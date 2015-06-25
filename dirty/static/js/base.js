        $( document ).ready(function() {
            function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
            $(".like_click").click(function(){

                var id = $(this).attr('id');
                var url = "{% url 'like_view' 12 %}".replace(12, id);
                var login_url = "{% url 'login_view' %}";
                var register_url = "{% url 'register_view' %}";
                var submit = $(this).data('value');
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {'submit': submit},
                    success: function(data){
                        if(data == "not_logged_in"){
                            $("#login_required").remove();
                            $(".rate_block"+id).append("<span id='login_required'><a href='"+login_url+"'>Войдите</a> или <a href='"+register_url+"'>зарегистрируйтесь</a>!</span>");
                        }
                        else{
                            $(".rate_block"+id+" > .vote_result").text(data);
                        }

                    }
                })
            });
            $('.add-favorite').on('click', function(){
                var self = $(this);
                var id = $(this).data('postid');
                var url = "{% url 'favorite_add_view' 12 %}".replace(12, id);
                 $.ajax({
                    url: url,
                    type: "POST",
                    success: function(data){
                        if(data === '_add'){
                            self.css('font-weight', 'bold')
                        }
                        else{
                            self.css('font-weight', '400')
                        }
                    }
                })
            });
        });

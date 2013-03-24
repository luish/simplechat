$(document).ready(function(){

    target = $('.messages');
    refresh(target);

    $('form#add-message').submit(function(){
        $.post('/messages/add', $(this).serialize(), 'json');
        $(this).children('#message').val('').focus();
        refresh(target);
        return false;
    });

    setInterval(function(){
        refresh(target);
    }, 2000);

    function refresh(target){
        $.get('/messages.json', function(data){
            list = '<ul>';
            $.each(data, function(i, message){
                list += '<li><strong>' + message.username + '</strong>: ' + message.message + '</li>';
            });
            list += '</ul>';

            target.html(list);

            // scroll to the end of the chat div
            target.scrollTop(target[0].scrollHeight);

        }, 'json');
    }

})
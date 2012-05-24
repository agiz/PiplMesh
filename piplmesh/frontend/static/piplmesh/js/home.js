function updateUserlist(data) {
	if (data.action == 'JOIN') {
		$('<li/>').text(data.username).appendTo('#userlist');
	}
	else if (data.action == 'PART') {
		// TODO: Improve escape and use more suitable :contains method
		$('#userlist li:contains(' + escape(data.username) + ')').remove();
	}
}

$(document).ready(function () {
	$.updates.registerProcessor('home_channel', 'userlist', updateUserlist);

    $.getJSON('/api/v1/post/',function(data){
        console.log(data);
        $.each(data, function(neki){
            if (neki == 'objects'){
                //alert(neki.length);
            }
        });
    });
});

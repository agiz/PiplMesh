$(document).ready(function() {
    $.getJSON(
        'http://odpiralnicasi.com/spots.json?callback=?',
        {
            lat: node.latitude,
            lng: node.longitude
        },
        function(data) {
            $.each(data['spots'], function (i, venue) {
                var venue_info = $('<span/>');
                var address = $('<p/>');
                if ('full_address' in venue) {
                    address.text(venue['full_address']);
                } else if ('street' in venue && 'city' in venue) {
                    address.text(venue['street']).append(", ");
                    address.append(venue['city']);
                }
                var name = $('<p/>');
                if ('combined_name' in venue) {
                    name.text(venue['combined_name']);
                } else if ('company' in venue && 'name' in venue) {
                    name.text(venue['company']);
                    name.append(venue['name']);
                } else if ('company' in venue || 'name' in venue) {
                    name.text(venue['company'] || venue['name']);
                }
                var days = ['open_mon', 'open_tue', 'open_wed', 'open_thu', 'open_fri', 'open_sat', 'open_sun'];
                var day_of_week = new Date().getDay();  //0=Sun, 1=Mon, ..., 6=Sat
                var today_label = $('<p/>').text(gettext("Today:")).append(" ");
                var today = $('<span/>').text(gettext('closed'));
                var open_hours = $('<dl/>');
                $.each(days, function (j, day) {
                    if (day in venue && venue[day].length > 0) {
                        if (day_of_week == (j+1)%7) {
                            today.text(venue[day]);
                        }
                        open_hours.append($('<dt/>').text(gettext(day.substr(5))).append(":"));
                        open_hours.append($('<dd/>').text(venue[day]));
                    }
                });
                today.append(" ").append($('<span/>').text(gettext("more")).click(function () {
                    today_label.html(open_hours);
                }));
                today_label.append(today);
                today_label.append();
                venue_info.append(name);
                venue_info.append(address);
                venue_info.append(today_label);
                var location = new google.maps.LatLng(venue.lat, venue.lng);
                var image = 'http://www.google.com/intl/en_us/mapfiles/ms/micons/yellow-dot.png';
                if ('is_open' in venue && venue['is_open'] == true) {
                    image = 'http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png';
                }
                var marker = new google.maps.Marker({
                    position: location,
                    map: map,
                    title: name.text(),
                    icon: image
                });
                google.maps.event.addListener(marker, 'click', function (event) {
                    $('#odpiralni_casi_info').html(venue_info).show();
                });
            });
        }
    );
});
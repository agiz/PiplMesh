// hover fix plugin
/*jQuery.fn.fixHover.js : for all elements, add hover class on mouseover and remove on mouseout */
jQuery.fn.fixHover = function(){
    $(this).each(function () {
        var hoverClasses = ' hover';
        if ($(this).attr('class')) {
            var classes = $(this).attr('class');
            var classArray = classes.split(' ');
            $(classArray).each(function () {
                hoverClasses += ' ' + this + 'Hover';
            });
        }
        $(this).hover(
        function() {
            if (classes) $(this).attr('class', classes + hoverClasses);
            else $(this).addClass('hover');
        },
        function() {
            if (classes) $(this).attr('class', classes);
            else $(this).removeClass('hover');
        }
        );
    });
}

map_loaded.done(function () {
    var shownVenues = {};

    function get_distance(d) {
        d += '';
        var multiplier = 1.0;
        if (d.toLowerCase().indexOf('km') > -1) {
            multiplier = 1000.0;
        }
        return parseFloat(d) * multiplier;
    }

    function toggleBounce(marker) {
        if (marker.getAnimation() != null) {
            marker.setAnimation(null);
        } else {
            marker.setAnimation(google.maps.Animation.BOUNCE);
            setTimeout(function(){ marker.setAnimation(null); }, 750);
        }
    }

    function Venue(data) {
        var self = this;
        $.extend(self, data);
        if ('distance' in self) {
            self.distance = get_distance(self.distance);
        }
        self.address = '';
        if ('full_address' in self) {
            self.address = self.full_address;
        } else if ('street' in self && 'city' in self) {
            self.address = self.street + ", " + self.city;
        }
        if ('combined_name' in self) {
            self.name = self.combined_name;
        } else if ('company' in self && 'name' in self) {
            self.name = self.company + " " + self.name;
        } else if ('company' in self || 'name' in self) {
            self.name = self.company || self.name;
        }
        self.today = self.is_open ? gettext("open") : gettext("closed");
        self.location = new google.maps.LatLng(self.lat, self.lng);
        self.image = 'https://www.google.com/intl/en_us/mapfiles/ms/micons/yellow-dot.png';
        if ('is_open' in self && self.is_open == true) {
            self.image = 'https://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png';
        }
        self.li = $('<li/>');
        self._key = [self.distance, self.name.toLowerCase()];
    }

    function redraw_venues() {
        var keys = [];
        $.each(shownVenues, function (key, venue) {
            if (map_edge < venue.distance) {
                return true;
            }
            keys.push(key);
        });
        keys.sort(function (key1, key2) {
            if (key1[0] < key2[0]) return 1;
            if (key1[0] > key2[0]) return -1;
            return 0;
        });
        $('#openhours_list').empty();

        var filterVenues = $('#filter_venues').val().toLowerCase();
        $.each(keys, function (i, key) {
            if (filterVenues === '' || key.indexOf(filterVenues) !== -1) {
                var venue = shownVenues[key];
                venue.li.html($('<a/>').prop('href', '#' + venue.sid).append(venue.name).click(function () {
                    toggleBounce(venue.marker);
                    return false;
                }));
                var div = $('<div/>').prop({
                    'class': 'info'
                });
                div.append(venue.address).append(" | ");
                var days = ['open_mon', 'open_tue', 'open_wed', 'open_thu', 'open_fri', 'open_sat', 'open_sun'];
                var day_of_week = new Date().getDay();  //0=Sun, 1=Mon, ..., 6=Sat
                var open_hours = $('<dl/>').prop({
                    'class': 'oh_tooltip'
                });
                $.each(days, function (j, day) {
                    if (day in venue && venue[day].length > 0) {
                        if (day_of_week == (j+1)%7) {
                            venue.today = venue[day];
                        }
                        open_hours.append($('<dt/>').text(gettext(day.substr(5))).append(":"));
                        open_hours.append($('<dd/>').text(venue[day]));
                    }
                });
                var today_label = $('<span/>').text(gettext("Today:")).append(" ");
                today_label.append(venue.today);
                today_label.hover(
                    function () {
                        $(this).parent().find('dl:hidden').css('top', venue.li.offset().top + 'px').fadeIn(500);
                    },
                    function () {
                        $(this).parent().find('dl:visible').fadeOut(500);
                    }
                );
                div.append(today_label);
                if (open_hours.children().length > 0) {
                    div.append(open_hours);
                }
                if ('sid' in venue) {
                    var website = 'http://odpiralnicasi.com/spots/' + venue.sid;
                    var website_image = $('<img/>').prop({
                        'src': '/static/piplmesh/panel/openhours/external_website.png',
                        'alt': website
                    });
                    div.append(" | ").append($('<a/>').prop('href', website).append(website_image));
                }

                venue.li.append(div);
                $('#openhours_list').append(venue.li);
            }
        });
    }

    $.getJSON(
        'http://odpiralnicasi.com/spots.json?callback=?',
        {
            lat: node.latitude,
            lng: node.longitude
        },
        function(data) {
            $.each(data['spots'], function (i, spot) {
                var venue = new Venue(spot);
                shownVenues[venue._key] = venue;
                var marker = new google.maps.Marker({
                    position: venue.location,
                    map: map,
                    title: venue.name,
                    icon: venue.image
                });
                venue.marker = marker;
                google.maps.event.addListener(marker, 'click', function (event) {
                    if (venue.li && venue.li.offset() && $('#openhours_list > li:first') && $('#openhours_list > li:first').offset()) {
                        $('#openhours_list').animate(
                            {
                                scrollTop: venue.li.offset().top - $('#openhours_list > li:first').offset().top
                            },
                            300,
                            function () {
                                if (venue.li.is(':visible')) {
                                    venue.li.effect('highlight', {}, 2000);
                                }
                            }
                        );
                    }
                });
            });
            $('#filter_venues').change(redraw_venues).keyup(redraw_venues);
            redraw_venues();
        }
    );
});
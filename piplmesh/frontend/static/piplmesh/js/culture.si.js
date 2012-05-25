var event = {};

function eventCleanTown(town) {
   return $.trim(town.split(/SI-[\d]{4}/)).substr(2);
}

var eventPlaceMarker = function(coords, args) {
    var defaultlocation = {lat: 46.17, lng: 14.96};
    if (coords.lat === defaultlocation.lat && coords.lng === defaultlocation.lng) {
        if (args[0] > 2) {
            return;
        }

        setTimeout(
            function(){
                rg.reversegeo(
                    'query',
                    {
                        'address': args[2].street+', '+eventCleanTown(args[2].town),
                        'callback': eventPlaceMarker,
                        'args': args
                    }
                )
            },
            1000*5*(args[0]*1+1)
        );
    } else {
        var titleArr = args[1].orgtitle || args[1].title;
        titleArr = titleArr.split(/\[\[(.+?)\]\]/g);
        var title = '';
        $.each(titleArr, function(i, item) {
            if (item.length > 0) {
                title += $.trim(item)+' ';
            }
        });
        title = $.trim(title);
        title = title.replace(/''/g, '');
        var website = args[2].website;
        var opts = { "title" : "Event " + title };
        var m = new google.maps.Marker(new google.maps.LatLng(coords.lat, coords.lng), opts);

        GEvent.addListener(m, "click", function() {
            html = '<div>'+title+'</div><div class="gmap_details">At: <span>'+args[1].at+'</span><br><a href="http://www.culture.si/en/'+args[1].link+'">more information</a>';
            if (args[1].program) html += ' | <a href="'+args[1].program+'">event homepage</a>';
            if (args[2].name) {
                if (args[2].email) {
                    html += '<br><a href="mailto:'+args[2].email+'">'+args[2].name+'</a>';
                } else {
                    html += '<br>'+args[2].name;
                }
            }
            if (website) html += ' | <a href="'+website+'">visit home page</a>';
            m.openInfoWindowHtml(html+'</div>');
        });
        gmap.addOverlay(m);
        updateMap();
    }
}

var rg = $(document).reversegeo({callback: alert});

function parseMarkerAttr(attr) {
    var attrArray = attr.split(/=(.+)/);
    var key = $.trim(attrArray[0]).toLowerCase();
    var value = $.trim(attrArray[1]);
    
    switch(key) {
        case 'email':
            break;
        case 'logo':
            break;
        case 'map':
            break;
        case 'name':
            break;
        case 'street':
            break;
        case 'telephone':
            break;
        case 'town':
            break;
        case 'website':
            break;
        default:
            return false;
    }
    
    return [key, value];
}

function eventPrepareMarker(tmpevent, data) {
    var boxArr = data.split(/\{\{ *Infobox/);
    
    if (boxArr[1] === undefined) {
        // TODO: This might cycle, not our problem per se but just in case.
        tmpevent.orgtitle = tmpevent.title;
        tmpevent.title = data;
        return eventDetail(tmpevent);
    }
    
    var tmpmarker = {};
    
    $.each(boxArr[1].split('}}')[0].split(/\n *\|/g), function(i, item) {
        if (i > 0) {
            var kv = parseMarkerAttr(item);
            if (kv) {
                tmpmarker[kv[0]] = kv[1];
            }
        }
    });

    if (tmpmarker.map) {
        var lat = tmpmarker.map.match(/lat=(\d+\.\d*)/)[1]*1;
        var lng = tmpmarker.map.match(/lon=(\d+\.\d*)/)[1]*1;
        if (lat && lng) {
            eventPlaceMarker({'lat': lat, 'lng': lng}, [99, tmpevent, tmpmarker]);
        }
    } else if (tmpmarker.street !== undefined && tmpmarker.town !== undefined && tmpmarker.town.length > 1) {
        var town = eventCleanTown(tmpmarker.town);
        if (town) {
            rg.reversegeo(
                'query',
                {
                    'address': tmpmarker.street+', '+town,
                    'callback': eventPlaceMarker,
                    'args': [0, tmpevent, tmpmarker]
                }
            );
        }
    }
}

function eventDetail(tmpevent) {
    var linkArr = tmpevent.title.match(/\[\[(.+?)\]\]/g);
    if (linkArr) {
        $.each(linkArr, function(i, item) {
            var eventUrl = item.substr(2, item.length-4).split('|')[0].replace(/ /g, '_');
            tmpevent['link'] = eventUrl;
            eventUrl = 'http://www.culture.si/en/api.php?action=query&prop=revisions&rvprop=content&titles='+eventUrl+'&format=json&callback=?';

            $.getJSON(
                eventUrl,
                function(data) {
                    for (var page in data.query.pages) {
                        break;
                    }
                       if (page == -1) {
                           return;
                       } else {
                           eventPrepareMarker(tmpevent, data.query.pages[page].revisions[0]['*']);
                       }
                }
            );
        });
    }
}

function eventIsRelevant(tmpevent) {
    return ((tmpevent.to === undefined) || (tmpevent.to < Date.today()) || (tmpevent.from > Date.parse('t + 31 d')));
}

function parseAttr(attr) {
    var attrArray = attr.split(/=(.+)/);
    var key = $.trim(attrArray[0]).toLowerCase();
    var value = $.trim(attrArray[1]);
    
    if (key.indexOf('category') == 0) {
        key = 'category';
    }
    
    switch(key) {
        case 'at':
            break;
        case 'category':
            value = value.toLowerCase();
            break;
        case 'from':
            value = Date.parse(value);
            break;
        case 'in':
            break;
        case 'program':
            break;
        case 'to':
            value = Date.parse(value);
            break;
        default:
            break;
    }
    
    return [key, value];
}

$(document).ready(function() {
    // Page id of upcoming events.
    var pageid = '483';
    $.getJSON(
        'http://www.culture.si/en/api.php?action=query&prop=revisions&rvprop=content&pageids='+pageid+'&format=json&callback=?',
        function(data) {
            var events = data.query.pages[pageid].revisions[0]['*'];
            var items = events.split(/upcomingEvent\n\| *[text|event]* *= */g);
            $.each(items, function(i,item) {
                if (i > 0) {
                    var tmpevent;
                    $.each(item.split(/\n *\|/g), function(j,subitem) {
                        if (j == 0) {
                            tmpevent = $.trim(subitem);
                            event[tmpevent] = {};
                            event[tmpevent]['title'] = tmpevent;
                        } else {
                            var kv = parseAttr(subitem);
                            if (kv[0] == 'category') {
                                if (event[tmpevent][kv[0]] === undefined) {
                                    event[tmpevent][kv[0]] = [];
                                }
                                event[tmpevent][kv[0]].push(kv[1]);
                            } else {
                                event[tmpevent][kv[0]] = kv[1];
                            }
                        }
                    });
                    if (eventIsRelevant(event[tmpevent])) {
                        delete event[tmpevent];
                    } else {
                        eventDetail(event[tmpevent]);
                    }
                }
            });
        }
    );
});
// shamelessly ripped from https://nodes.wlan-si.net/js/map.js

var updating = false;
var centering = false;
var shownNodes = {};
var shownNodesNumber = 0;

var gmap;

function updateNodes(filtersChanged, zoomChanged, moved) {
    if (filtersChanged) {
        gmap.clearOverlays();
        
        shownNodes = {};
        shownNodesNumber = 0;
        for (var i = 0; i < nodes.length; i++) {
            shownNodes[nodes[i].ip] = nodes[i];
            shownNodesNumber++;
            createMarker(nodes[i]);
        }
    }
}

function centerMap() {
    var id = $('#gmap_center').val();

    if (!id) return;
    
    var bounds = new google.maps.LatLngBounds();
    var count = 0;
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].project == id) {
            bounds.extend(new google.maps.LatLng(nodes[i].lat, nodes[i].long));
            count++;
        }
    }
    
    // To be robust if user manages to select disabled center map entry
    if (!count) return;
    
    if ($('#gmap_project_' + id + ':checked').length == 0) {
        updating = true;
        $('#gmap_project_' + id).attr('checked', 'checked');
        updating = false;
    }
    
    $('#gmap_center_default').attr('disabled', 'disabled');
}

function updateMap() {
    if (updating) return;
}

function mapInit(map) {
    gmap = map;
    var lock = false;

    $(document).ready(function () {
        $('#gmap_center').change(centerMap);
        
        var currentParams = {};
        var randomNode = nodes[Math.floor(Math.random() * nodes.length)];
        var filtersChanged = true;
        var zoomChanged = false;
        var moved = false;
        
        currentParams.lat = randomNode.lat;
        currentParams.long = randomNode.long;
        currentParams.zoom = 15;
        currentParams.type = gmap.getCurrentMapType();

        updating = true;
        gmap.setCenter(
            new google.maps.LatLng(
                currentParams.lat,
                currentParams.long
            ),
            parseInt(currentParams.zoom),
            currentParams.type
        );
        updating = false;
        updateNodes(
            filtersChanged,
            zoomChanged,
            moved
        );
        updateMap();
    });
}
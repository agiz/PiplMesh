/* jQuery Simple-Geolocation
 *
 * @author Ziga Zupanec <ziga.zupanec@gmail.com>
 * @public domain
 * @version 0.1
 */

;(function($) {
    var defaultlocation = {lat: 46.17, lng: 14.96, zoom: 8};

    var methods = {
        init: function(params) {
            return this.each(function(){
                var $this = $(this),
                    data = $this.data('simplegeo'),
                    simplegeo = $this;
                
                if (!data) {
                    if (params.callback === undefined) {
                        params.callback = alert;
                    }
                    if (params.zoom === undefined) {
                        params.zoom = defaultlocation.zoom;
                    }
                    if (params.lat === undefined || params.lng === undefined) {
                        params.lat = false || params.lat;
                        params.lng = false || params.lng;

                        var nodeResponse = $this.simplegeo('node');
                        if (nodeResponse) {
                            params.callback(nodeResponse);
                        }
                        else {
                            $this.simplegeo('html5', params.callback);
                        }
                    }
                    else {
                        params.callback({lat: params.lat, lng: params.lng, zoom: params.zoom});
                    }
                }
            });
        },

        node: function() {
            // TODO: Remove stub.
            if (Math.random() < 0.5)
                return false;
            var randomNode = nodes[Math.floor(Math.random() * nodes.length)];
            return {lat: randomNode.lat, lng: randomNode.long, zoom: 15};
        },
        
        html5: function(callback) {
            if (navigator.geolocation)
            {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        callback({lat: position.coords.latitude, lng: position.coords.longitude, zoom: 15});
                    },
                    function(msg) {
                        callback(defaultlocation);
                    }
                );
            }
            else {
                callback(defaultlocation);
            }
        },
        
        update: function(params) {
            return this.each(function() {
                var $this = $(this),
                    data = $this.data('simplegeo');

                if (params === undefined)
                    params = data;

                $(this).data('simplegeo', {
                    target: $this,
                    lat: params.lat || data.lat,
                    lng: params.lng || data.lng,
                    zoom: params.zoom || data.zoom
                });
            })
        }
    };

    $.fn.simplegeo = function(method) {
        if (methods[method]) {
            return methods[method].apply(
                this,
                Array.prototype.slice.call(arguments, 1)
            );
        }
        else if (typeof method === 'object' || !method) {
            return methods.init.apply(
                this,
                arguments
            );
        }
        else {
            $.error('Method '+method+' does not exist on jQuery.simplegeo');
        }
    };
})(jQuery);
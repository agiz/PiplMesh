/* jQuery Reverse-Geolocation
 *
 * @author Ziga Zupanec <ziga.zupanec@gmail.com>
 * @based on http://viralpatel.net/blogs/demo/google-map-reverse-geocoding.html
 * @public domain
 * @version 0.1
 */

;(function($) {
    var defaultlocation = {lat: 46.17, lng: 14.96};
    var geocoder = null;
    var callback = alert;

    var methods = {
        init: function(params) {
            return this.each(function(){
                var $this = $(this),
                    data = $this.data('reversegeo'),
                    reversegeo = $this;
                
                if (!data) {
                    if (GBrowserIsCompatible()) {
                        geocoder = new GClientGeocoder();
                        if (params !== undefined && params.callback !== undefined) {
                            callback = params.callback;
                        }
                    }
                }
            });
        },

        query: function(params) {
            return this.each(function() {
                var myLocation;
                var $this = $(this),
                    data = $this.data('reversegeo');

                if (params.address === undefined || !geocoder) {
                    params.callback(defaultlocation, params.args);
                } else {
                    geocoder.getLocations(params.address, function(response) {
                        if (!response || response.Status.code != 200) {
                            myLocation = defaultlocation;
                            params.args[0]++;
                        } else {
                            place = response.Placemark[0];
                            myLocation = {
                                lat: place.Point.coordinates[1],
                                lng: place.Point.coordinates[0]
                            };
                        }
                        params.callback(myLocation, params.args);
                    });
                }
            })
        }
    };

    $.fn.reversegeo = function(method) {
        if (methods[method]) {
            return methods[method].apply(
                this,
                Array.prototype.slice.call(arguments, 1)
            );
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(
                this,
                arguments
            );
        } else {
            $.error('Method '+method+' does not exist on jQuery.reversegeo');
        }
    };
})(jQuery);
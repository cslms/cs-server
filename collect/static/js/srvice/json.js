// Define the encode(), decode(), dumps() and loads() functions
var srvice$json = (function($) {
    // The library requires a dictionary with conversions for each supported
    // data type. This extends plain JSON to types that are not natively
    // supported by converting then to an dictionary with a {'@': type-name}
    // key/value pair.
    var json_converters = {
        // Javascript objects. You might need to encode if they have a "@" key
        object: {
            constructor: Object,
            encode: function(x) {
                var out = {};

                for (key in x) {
                    out[key] = json_codec_worker(json[key], true);
                }

                return {'@': 'object', data: out};
            },
            decode: function(x) {
                return x.data || {};
            }
        },

        // Javascript dates
        date: {
            constructor: Date,
            encode: function(x) {
                return {
                    time: x.getTime(),
                    timezone: x.getTimezoneOffset()
                };
            },
            decode: function(x) {
                return new Date(x.time + x.timezone);
            }
        }
    };

    // Encode/decode JSON like structures. Do not follow inheritance since it tends
    // to be broken in js.
    function encode(x) {
        /**:srvice.json.encode(obj)

            Encode object into a JSON-compatible structure.
         */
        return json_codec_worker(x, true)
    }


    function decode(x) {
        /**:srvice.json.decode(obj)

            Return the Javascript object equivalent to the given
            JSON-compatible structure.

         */
        return json_codec_worker(x, false)}


    function json_codec_worker(json, encode) {
        var decode = !encode;
        var out, key;

        // Don't like undefined values
        if (json === undefined) {
            throw "cannot " + (encode? "encode": "decode") + " undefined values";
        }

        // Return valid atomic types (but not subtypes)
        if (json === null) {
            return null;
        }

        if ([String, Number, Boolean].includes(json.constructor)) {
            return json;
        }

        // Convert arrays recursively
        if (json instanceof Array) {
            return $.map(json, function(x) {
                return [json_codec_worker(x, encode)];
            });
        }

        // Encode objects recursively
        if (json.constructor === Object && encode) {
            out = {};
            for (key in json) {
                out[key] = json_codec_worker(json[key], true);
            }
            if ('@' in json) {
                out = {'@': object, data: out};
            }
            return out;
        }

        // Decode objects
        if (json.constructor === Object && decode) {
            if ('@' in json) {
                var decoder = json['@'];
                delete json['@'];
                return  json_converters[decoder].decode(out);
            }

            out = {};
            for (key in json) {
                out[key] = json_codec_worker(json[key], false);
            }
            return out;
        }

        // Convert arbitrary JS types
        if (encode) {
            for (var name in  json_converters) {
                var conv =  json_converters[name];

                if (json.constructor === conv.constructor) {
                    var encoded = conv.encode(json);
                    encoded['@'] = name;
                    return encoded;
                }
            }
        }

        // Give up
        if (encode) {
            throw "cannot serialize to json: " + json;
        } else {
            throw "not a JSON element: " + json;
        }
    }


    function dumps(obj) {
        /**:srvice.json.dumps(obj)

            Stringfy javascript object to a JSON stream.
         */

        var encoded = encode(obj);
        return JSON.stringify(encoded);
    }


    function loads(data) {
        /**:srvice.json.loads(String data)

            Load javascript object from a JSON encoded string.
         */

        var encoded = $.parseJSON(data);
        return decode(encoded);
    }

    return {encode: encode, decode: decode, loads: loads, dumps: dumps}
}(jQuery));
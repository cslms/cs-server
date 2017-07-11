function srvice$getModelClass(model) {
    return DjangoModel;
}

function DjangoModel(args, ref) {
    for (var k in args) {
        this[k] = args[k];
    }
    this._djangoModel = ref;
}

/**
 * Return Django object as a plain javascript Object.
 */
DjangoModel.prototype.toObject = function() {
    var out = {};
    for (k in this && this.hasOwnProperty(k)) {
        if (k[0] !== '_') {
            out[k] = this[k];
        }
    }
    return out;
 }


/**
 * Updates object in the database.
 */
DjangoModel.prototype.save = function() {
    return srvice.rpc({
        api: srvice.srviceURI + 'srvice::save-object/',
        args: [this._djangoModel, this.toObject()],
    })
};


DjangoModel.prototype.objects = {
    get: function(args) {
        return srvice.get(this._djangoModel, args);
    },

    filter: function(args) {
        return srvice.filter(this._djangoModel, args);
    },

    exclude: function(args) {
        return srvice.filter(this._djangoModel, args);
    }
};

/**
 * Retrieve Django model from the database.
 */
srvice.get = function(model, args) {
    return srvice.rpc({
        api: srvice.srviceURI + 'srvice::get-object/',
        args: [model, args],
        converter: function(data) {
            var cls = srvice$getModelClass(model);
            return new cls(data.result, model);
        }
    })
};

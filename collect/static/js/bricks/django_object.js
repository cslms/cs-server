function bricks$getModelClass(model) {
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
    return bricks.rpc({
        api: bricks.bricksURI + 'bricks::save-object/',
        args: [this._djangoModel, this.toObject()],
    })
};


DjangoModel.prototype.objects = {
    get: function(args) {
        return bricks.get(this._djangoModel, args);
    },

    filter: function(args) {
        return bricks.filter(this._djangoModel, args);
    },

    exclude: function(args) {
        return bricks.filter(this._djangoModel, args);
    }
};

/**
 * Retrieve Django model from the database.
 */
bricks.get = function(model, args) {
    return bricks.rpc({
        api: bricks.bricksURI + 'bricks::get-object/',
        args: [model, args],
        converter: function(data) {
            var cls = bricks$getModelClass(model);
            return new cls(data.result, model);
        }
    })
};

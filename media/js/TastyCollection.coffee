define ['api'], (api) ->
    class TastyCollection extends Backbone.Collection

        url : ->
            @urlRoot = api.getResourceUrl(@model.resourceName)
            return super()


    return TastyCollection

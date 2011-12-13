define ['api'], (api) ->
    class TastyCollection extends Backbone.Collection

        url : ->
            api.getResourceUrl(@model.resourceName)

        parse : (response) ->
            parsedObjectData = (@model.parse data for data in response.objects)
            super(parsedObjectData)

    return TastyCollection

define ['api'], (api) ->

    class TastyModel extends Backbone.Model

        url : ->
            url = super() or api.getResourceUrl(@constructor.resourceName)
            return url

    return TastyModel

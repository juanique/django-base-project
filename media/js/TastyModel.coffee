define ['api'], (api) ->

    class TastyModel extends Backbone.Model

        url : ->
            url = super()
            if not url
                return api.getResourceUrl(@constructor.resourceName)

    return TastyModel

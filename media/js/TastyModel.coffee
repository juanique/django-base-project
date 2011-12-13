define ['api'], (api) ->

    class TastyModel extends Backbone.Model

        url : ->
            url = api.getResourceUrl(@constructor.resourceName)
            if @id
                url += "#{@id}/"
            return url

    return TastyModel

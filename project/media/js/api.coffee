define ->
    class Api
        baseUrl : "/api/resources"

        getResourceUrl : (resourceName) ->
            return "#{@baseUrl}/#{resourceName}/"

 
    return new Api()

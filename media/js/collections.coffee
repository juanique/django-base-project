define ['api','models', 'TastyCollection'], (api, models, TastyCollection) ->

    class Users extends TastyCollection
        model: models.User

    return {
        Users : Users
    }

define ['api','TastyModel'], (api,TastyModel) ->

    class User extends TastyModel
        @resourceName : 'user'

        @parse : (data) ->
            delete data['password'] if data['password'] isnt undefined

        parse : (data) ->
            return super(User.parse(data))


    return {
        User: User
    }

require ['collections','models'], (collections, models) ->
    console.log "hola"
    users = new collections.Users()
    users.url()
    users.fetch()

    window.users = users
    window.User = models.User

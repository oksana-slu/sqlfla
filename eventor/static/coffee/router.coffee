'use strict'

class EventorRouter extends Backbone.Router
  routes:
    "events/new":   "nothing"
    "events/:id":   "showEvent"
    "events/*action": "nothing"

  nothing: (options) ->
    console.log "EventorRouter#nothing", options

  showEvent: (eventId) ->
    usersView = new UsersView
      event: eventId
      el: $(".participants")

$ ->
  eventRouter = new EventorRouter()
  Backbone.history.start(pushState: true)

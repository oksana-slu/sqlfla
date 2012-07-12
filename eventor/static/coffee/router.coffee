'use strict'

class EventorRouter extends Backbone.Router
  routes:
    "events/new":   "nothing"
    "events/:id/?page=:page":   "showEvent"
    "events/:id/":   "showEvent"
    "events/*action": "nothing"

  nothing: (options) ->
    console.log "EventorRouter#nothing", options

  showEvent: (eventId, page=1) ->
    usersView = new UsersView
      event: eventId
      page: page
      el: $(".participants")

$ ->
  eventRouter = new EventorRouter()
  Backbone.history.start(pushState: true)

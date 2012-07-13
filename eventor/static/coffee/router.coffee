'use strict'

class EventorRouter extends Backbone.Router
  routes:
    "events/new":   "nothing"
    "events/:id/?page=:page&p_type=:p_type":   "showEvent"
    "events/:id/":   "showEvent"
    "events/*action": "nothing"

  nothing: (options) ->
    console.log "EventorRouter#nothing", options

  showEvent: (eventId, page=1, p_type=0) ->
    usersView = new UsersView
      event: eventId
      page: page
      p_type: p_type
      el: $(".participants")

$ ->
  eventRouter = new EventorRouter()
  Backbone.history.start(pushState: true)

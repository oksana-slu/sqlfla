'use strict'

usersTemplate = _.template("""
<ul class="unstyled">
  <% _(users).each(function(user) { %>
    <li>
        <%= user.first_name + ' ' + user.last_name %>
        <a href="#" rel="tooltip" title="Approve" data-value='approve'><i class="icon-ok-sign"></i></a>
        <a href="#" rel="tooltip" title="Decline" data-value='decline'><i class="icon-remove-sign"></i></a>
    </li>
  <% }) %>
</ul>
""")
# -----------------------------------------------------------------------------
class Users extends Backbone.Collection
  model: Backbone.Model
  url: '/events/participants/'

  parse: (response) ->
    @meta = response.meta
    response.objects
# -----------------------------------------------------------------------------
class UsersView extends Backbone.View
  className: 'span5'
  template: usersTemplate
  collection: new Users

  events:
    "click a": "resolveParticipant"


  initialize: (options) ->
    console.log options.el
    @collection.on 'reset', => @render()
    @collection.fetch
      data:
        event: options.event


  render: ->
    @$el.hide()

    @$el.html @template
      users: @collection.toJSON()
    console.log @el
    @$el.find("a[rel='tooltip']").tooltip()
    @$el.fadeIn()

    @el


  resolveParticipant: (ev) ->
    ev.preventDefault()
    console.log $(ev.currentTarget).data('value')
# -----------------------------------------------------------------------------

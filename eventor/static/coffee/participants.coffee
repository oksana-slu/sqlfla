'use strict'

usersTemplate = _.template("""
<ul class="unstyled">
  <div class="pagination pagination-centered">
    <ul>
      <% _.each(_.range(1, paginations['pages'] + 1), function(page) { %>
      <li <% if (page == paginations['page']) { %> class="active" <% } %> >
        <a class="numb-page" href="?page=<%= page %>" data-value="<%= page %>"><%= page %></a>
      </li>
      <% }) %>
    </ul>
  </div>
  <% _(users).each(function(user) { %>
    <li>
        <%= user.first_name + ' ' + user.last_name %>
        <a class="resolve" href="#" rel="tooltip" title="Approve" data-value='approve'><i class="icon-ok-sign"></i></a>
        <a class="resolve" href="#" rel="tooltip" title="Decline" data-value='decline'><i class="icon-remove-sign"></i></a>
    </li>
  <% }) %>
  <div class="pagination pagination-centered">
    <ul>
      <% _.each(_.range(1, paginations['pages'] + 1), function(page) { %>
      <li <% if (page == paginations['page']) { %> class="active" <% } %> >
        <a class="numb-page" href="?page=<%= page %>" data-value="<%= page %>"><%= page %></a>
      </li>
      <% }) %>
    </ul>
  </div>
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
    "click a.resolve": "resolveParticipant"
    "click a.numb-page": "numbPage"


  initialize: (options) ->
    @event = options.event
    console.log options.el
    @collection.on 'reset', => @render()
    @collection.fetch
      data:
        event: options.event
        page: options.page


  render: ->

    @$el.html @template
      users: @collection.toJSON()
      paginations: @collection.meta
    console.log @el
    @$el.find("a[rel='tooltip']").tooltip()
    @$el.fadeIn()

    @el


  resolveParticipant: (ev) ->
    ev.preventDefault()
    console.log $(ev.currentTarget).data('value')


  numbPage: (ev) ->
    ev.preventDefault()
    page = $(ev.currentTarget).data('value')
    @collection.fetch
      data:
        event: @event
        page: page
    history.pushState(null,null,"?page=" + page)
# -----------------------------------------------------------------------------

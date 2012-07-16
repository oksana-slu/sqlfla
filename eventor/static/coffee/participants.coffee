'use strict'

usersTemplate = _.template("""
<div class="row">
  <div class="span5"><h3>Event participants (<%= paginations['total'] %>)</h3></div>
  <div class="span5">
    <div class="btn-group" data-toggle="buttons-radio">
      <button class="btn <% if (p_type == 1) { %> active <% } %>" data-value=1>Approved</button>
      <button class="btn <% if (p_type == 0) { %> active <% } %>" data-value=0>Awaiting</button>
      <button class="btn <% if (p_type == 2) { %> active <% } %>" data-value=2>Declined</button>
    </div>
  </div>
</div>
<div class="row">
  <ul class="unstyled">
    <div class="pagination pagination-centered">
      <ul>
        <% _.each(_.range(1, paginations['pages'] + 1), function(page) { %>
        <li <% if (page == paginations['page']) { %> class="active" <% } %> >
          <a class="numb-page" href="#" data-value="<%= page %>"><%= page %></a>
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
</div>
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
    "click button.btn": "typeFilter"


  initialize: (options) ->
    @event = options.event
    @p_type = options.p_type

    @collection.on 'reset', => @render()
    @collection.fetch
      data: options

  render: ->

    @$el.html @template
      users: @collection.toJSON()
      paginations: @collection.meta
      p_type: @p_type

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
    history.pushState(null, null, "?#{$.param(page: page, p_type: @p_type)}")


  typeFilter: (ev) ->
    @p_type = $(ev.currentTarget).data('value')
    @collection.fetch
      data:
        event: @event
        p_type: @p_type
    history.pushState(null,null,"?#{$.param(page: 1, p_type: @p_type}")
# -----------------------------------------------------------------------------

var adjustWidth;

adjustWidth = function() {
  return _($(".input-append")).each(function(el, idx) {
    var $el, $input, addonWidth, inputWidth;
    $el = $(el);
    $input = $el.find("input");
    inputWidth = parseInt($input.innerWidth());
    addonWidth = parseInt($el.find(".add-on").innerWidth());
    return $input.css('width', inputWidth - addonWidth - 6);
  });
};

$(function() {
  $(".event textarea").css('height', 184);
  $("input[type='datetime-local']").mask("99.99.9999 99:99");
  $("form").on('submit', function(ev) {
    return $(ev.currentTarget).find("[type='submit']").button('loading');
  });
  return $("[rel='tooltip']").tooltip();
});

'use strict';

var Users, UsersView, usersTemplate,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

usersTemplate = _.template("<ul class=\"unstyled\">\n  <% _(users).each(function(user) { %>\n    <li>\n        <%= user.first_name + ' ' + user.last_name %>\n        <a href=\"#\" rel=\"tooltip\" title=\"Approve\" data-value='approve'><i class=\"icon-ok-sign\"></i></a>\n        <a href=\"#\" rel=\"tooltip\" title=\"Decline\" data-value='decline'><i class=\"icon-remove-sign\"></i></a>\n    </li>\n  <% }) %>\n</ul>");

Users = (function(_super) {

  __extends(Users, _super);

  function Users() {
    return Users.__super__.constructor.apply(this, arguments);
  }

  Users.prototype.model = Backbone.Model;

  Users.prototype.url = '/events/participants/';

  Users.prototype.parse = function(response) {
    this.meta = response.meta;
    return response.objects;
  };

  return Users;

})(Backbone.Collection);

UsersView = (function(_super) {

  __extends(UsersView, _super);

  function UsersView() {
    return UsersView.__super__.constructor.apply(this, arguments);
  }

  UsersView.prototype.className = 'span5';

  UsersView.prototype.template = usersTemplate;

  UsersView.prototype.collection = new Users;

  UsersView.prototype.events = {
    "click a": "resolveParticipant"
  };

  UsersView.prototype.initialize = function(options) {
    var _this = this;
    console.log(options.el);
    this.collection.on('reset', function() {
      return _this.render();
    });
    return this.collection.fetch({
      data: {
        event: options.event
      }
    });
  };

  UsersView.prototype.render = function() {
    this.$el.hide();
    this.$el.html(this.template({
      users: this.collection.toJSON()
    }));
    console.log(this.el);
    this.$el.find("a[rel='tooltip']").tooltip();
    this.$el.fadeIn();
    return this.el;
  };

  UsersView.prototype.resolveParticipant = function(ev) {
    ev.preventDefault();
    return console.log($(ev.currentTarget).data('value'));
  };

  return UsersView;

})(Backbone.View);

'use strict';

var EventorRouter,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

EventorRouter = (function(_super) {

  __extends(EventorRouter, _super);

  function EventorRouter() {
    return EventorRouter.__super__.constructor.apply(this, arguments);
  }

  EventorRouter.prototype.routes = {
    "events/new": "nothing",
    "events/:id": "showEvent",
    "events/*action": "nothing"
  };

  EventorRouter.prototype.nothing = function(options) {
    return console.log("EventorRouter#nothing", options);
  };

  EventorRouter.prototype.showEvent = function(eventId) {
    var usersView;
    return usersView = new UsersView({
      event: eventId,
      el: $(".participants")
    });
  };

  return EventorRouter;

})(Backbone.Router);

$(function() {
  var eventRouter;
  eventRouter = new EventorRouter();
  return Backbone.history.start({
    pushState: true
  });
});

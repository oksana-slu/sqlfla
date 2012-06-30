

adjustWidth = ->
  _($ ".input-append").each (el, idx) ->
    $el = $ el
    $input = $el.find("input")
    inputWidth = parseInt $input.innerWidth()
    addonWidth = parseInt $el.find(".add-on").innerWidth()
    $input.css 'width', (inputWidth - addonWidth - 6)

$ ->
  $(".event textarea").css('height', 184)
  # adjustWidth()
  $("input[type='datetime-local']").mask("99.99.9999 99:99")

  $("form").on 'submit', (ev) ->
    $(ev.currentTarget).find("[type='submit']").button 'loading'



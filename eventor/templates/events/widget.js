(function (global, oDOC, handler) {
    var head = oDOC.head || oDOC.getElementsByTagName("head");

    function LABjsLoaded() {
      $LAB.script("https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js").wait(function() {
        var $container = $("#{{ container }}");
          $container.css(
            {width: 250, height: 300, border: 'solid 1px #000'}
          ).append(
            $('<div>').css({'margin': '3px', 'font': 'bold 11pt sans-serif'})
              .text("{{ event.name }}!")
          ).append(
            $('<div>').css({'margin': '3px 12px', 'font': 'normal 10pt sans-serif', 'text-align': 'right'})
              .text("{{ event.starts_at.strftime('%d.%m.%Y') }}")
          ).append(
            $('<div>')
              .append(
                $('<form>').attr({name: 'evForm_{{ event.id }}'})
                  .append('<input>').attr({name: 'email'})
              )
          );

      });
    }

    // loading code borrowed directly from LABjs itself
    setTimeout(function () {
        if ("item" in head) { // check if ref is still a live node list
            if (!head[0]) { // append_to node not yet ready
                setTimeout(arguments.callee, 25);
                return;
            }
            head = head[0]; // reassign from live node list ref to pure node ref -- avoids nasty IE bug where changes to DOM invalidate live node lists
        }
        var scriptElem = oDOC.createElement("script"),
            scriptdone = false;
        scriptElem.onload = scriptElem.onreadystatechange = function () {
            if ((scriptElem.readyState && scriptElem.readyState !== "complete" && scriptElem.readyState !== "loaded") || scriptdone) {
                return false;
            }
            scriptElem.onload = scriptElem.onreadystatechange = null;
            scriptdone = true;
            LABjsLoaded();
        };
        scriptElem.src = "http://localhost:5000/static/js/vendor/LAB.min.js";
        head.insertBefore(scriptElem, head.firstChild);
    }, 0);

    // required: shim for FF <= 3.5 not having document.readyState
    if (oDOC.readyState === null && oDOC.addEventListener) {
        oDOC.readyState = "loading";
        oDOC.addEventListener("DOMContentLoaded", handler = function () {
            oDOC.removeEventListener("DOMContentLoaded", handler, false);
            oDOC.readyState = "complete";
        }, false);
    }
})(window, document);

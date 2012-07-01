(function (global, oDOC, handler) {
    var head = oDOC.head || oDOC.getElementsByTagName("head");

    function LABjsLoaded() {
      $LAB.script("https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js").wait(function() {
        var iTxtStyle = {
          display: 'inline-block',
          margin: '5px',
          'background-color': 'white',
          'border': '1px solid #CCC',
          '-webkit-border-radius': '3px',
          '-moz-border-radius': '3px',
          'border-radius': '3px',
          '-webkit-box-shadow': 'inset 0 1px 1px rgba(0, 0, 0, 0.075)',
          '-moz-box-shadow': 'inset 0 1px 1px rgba(0, 0, 0, 0.075)',
          'box-shadow': 'inset 0 1px 1px rgba(0, 0, 0, 0.075)',
          '-webkit-transition': 'border linear 0.2s, box-shadow linear 0.2s',
          '-moz-transition': 'border linear 0.2s, box-shadow linear 0.2s',
          '-ms-transition': 'border linear 0.2s, box-shadow linear 0.2s',
          '-o-transition': 'border linear 0.2s, box-shadow linear 0.2s',
          'transition': 'border linear 0.2s, box-shadow',
          'height': '18px',
          'padding': '4px',
          'margin-bottom': '9px',
          'font-size': '13px',
          'line-height': '18px',
          'color': '#555',
          'font-family': '"Helvetica Neue", Helvetica, Arial, sans-serif'
        }, iLablStyle = {
          'float': 'left',
          'width': '75px',
          'padding-top': '9px',
          'text-align': 'right',
          'display': 'block',
          'margin-bottom': '5px',
          'font-size': '13px',
          'font-weight': 'normal',
          'line-height': '18px',
          'font-family': '"Helvetica Neue", Helvetica, Arial, sans-serif',
          'color': '#333'
        }, grpStyle = {
          'display': 'table'
        }, ctrlStyle = {
          'margin-left': '80px'
        }, btnStyle = {
          '-webkit-box-shadow': '-2px 2px 0 #612C0C',
          '-moz-box-shadow': '-2px 2px 0 #612c0c',
          'box-shadow': '-2px 2px 0 #612C0C',
          'text-shadow': 'none',
          'background-image': 'none',
          'border': 'none',
          'background-color': '#E37E23',
          'background-image': '-moz-linear-gradient(top, #E36B23, #E39B23)',
          'background-image': '-ms-linear-gradient(top, #E36B23, #E39B23)',
          'background-image': '-webkit-gradient(linear, 0 0, 0 100%, from(#E36B23), to(#E39B23))',
          'background-image': '-webkit-linear-gradient(top, #E36B23, #E39B23)',
          'background-image': '-o-linear-gradient(top, #E36B23, #E39B23)',
          'background-image': 'linear-gradient(top, #E36B23, #E39B23)',
          'background-repeat': 'repeat-x',
          'filter': "progid:DXImageTransform.Microsoft.gradient(startColorstr='#e36b23', endColorstr='#e39b23', GradientType=0)",
          'border-color': '#E39B23 #E39B23 #A56F15',
          'border-color': 'rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.25)',
          'display': 'inline-block',
          'padding': '4px 10px 4px',
          'margin-bottom': '0',
          'font-size': '15px',
          'line-height': '20px',
          'vertical-align': 'middle',
          'cursor': 'pointer',
          '-webkit-border-radius': '4px',
          '-moz-border-radius': '4px',
          'border-radius': '4px',
          'margin-left': '60px'
        };
        var $container = $("#{{ container }}");
          $container.css(
            {width: 250, height: 320, border: 'solid 1px #000'}
          ).append(
            $('<div>').css({'margin': '3px', 'font': 'bold 11pt sans-serif'})
              .text("{{ event.name }}!"),
            $('<div>').css({'margin': '3px 12px', 'font': 'normal 10pt sans-serif', 'text-align': 'right'})
              .text("{{ event.starts_at.strftime('%d.%m.%Y') }}"),
            $('<div>')
              .append(
                $('<form>').attr({name: 'evForm_{{ event.id }}'})
                  .append(
                    $('<div>').append(
                      $('<label>').text('Email:').attr({'for': 'email_{{container}}'}).css(iLablStyle),
                      $('<div>').append(
                        $('<input>').attr({name: 'email', type: 'text', 'id': 'email_{{container}}'}).css(iTxtStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle),
                    $('<div>').append(
                      $('<label>').text('First Name:').attr({'for': 'first_{{container}}'}).css(iLablStyle),
                      $('<div>').append(
                        $('<input>').attr({name: 'first', type: 'text', 'id': 'first_{{container}}'}).css(iTxtStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle),
                    $('<div>').append(
                      $('<label>').text('Last Name:').attr({'for': 'last_{{container}}'}).css(iLablStyle),
                      $('<div>').append(
                        $('<input>').attr({name: 'last', type: 'text', 'id': 'last_{{container}}'}).css(iTxtStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle),
                    $('<div>').append(
                      $('<label>').text('Occupation:').attr({'for': 'occupe_{{container}}'}).css(iLablStyle),
                      $('<div>').append(
                        $('<input>').attr({name: 'occupe', type: 'text', 'id': 'occupe_{{container}}'}).css(iTxtStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle),
                    $('<div>').append(
                      $('<label>').text('Company:').attr({'for': 'company_{{container}}'}).css(iLablStyle),
                      $('<div>').append(
                        $('<input>').attr({name: 'company', type: 'text', 'id': 'company_{{container}}'}).css(iTxtStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle),
                    $('<div>').append(
                      $('<div>').append(
                        $('<input>').attr({type: 'submit'}).val("I'll attend").css(btnStyle)
                      ).css(ctrlStyle)
                    ).css(grpStyle)

                  )
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

from flask.ext.assets import Bundle


bootstrap = {
    'prefix': "bootstrap/js/",
    'files': [
        "bootstrap-transition.js",
        "bootstrap-alert.js",
        "bootstrap-button.js",
        "bootstrap-carousel.js",
        "bootstrap-collapse.js",
        "bootstrap-dropdown.js",
        "bootstrap-modal.js",
        "bootstrap-scrollspy.js",
        "bootstrap-tab.js",
        "bootstrap-tooltip.js",
        "bootstrap-popover.js",
        "bootstrap-typeahead.js"]
}

vendor = {
    'prefix': "js/vendor/",
    'files': [
        'jquery-1.7.1.js',
        'underscore-1.3.3.js',
        'backbone-0.9.2.js',
        'chosen.jquery-0.9.8.js',
        'jquery.maskedinput.js',
        'handlebars-1.0.0.beta.6.js',
        'less-1.3.0.js',
#        'require-1.0.7.js',
#        'require-text-1.0.7.js',
    ]
}


user = {
    'prefix': "coffee/",
    'files': [
        'common.coffee'
    ]
}

user_js = Bundle(
    *[user['prefix'] + script for script in user['files']],
    filters="coffeescript, uglifyjs",
    output="gen/user.js"
)

bootstrap_js = Bundle(
    *[bootstrap['prefix'] + script for script in bootstrap['files']],
    filters="uglifyjs",
    output="gen/bootstrap.js"
)

vendor_js = Bundle(
    *[vendor['prefix'] + script for script in vendor['files']],
    filters="uglifyjs",
    output="gen/vendor.js"
)

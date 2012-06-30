from flask.ext.assets import Bundle


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
        'bootstrap.js'
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

vendor_js = Bundle(
    *[vendor['prefix'] + script for script in vendor['files']],
    filters="uglifyjs",
    output="gen/vendor.js"
)

#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from eventor import app, assets
from eventor.commands import CreateSuperuser, InitDB

manager = Manager(app)

manager.add_command('assets', ManageAssets(assets))
manager.add_command('create_superuser', CreateSuperuser())
manager.add_command('init_db', InitDB())

if __name__ == '__main__':
    manager.run()

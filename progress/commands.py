# -*- coding: utf-8 -*-
import click
from werkzeug.security import generate_password_hash, check_password_hash
from progress import app, db
from progress.models import User, Project


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Grey Li'
    user_name = 'michael'
    passwd = '123'
    projects = [
        {'title': 'My Neighbor Totoro', 'total': 100, 'progress': 0},
        {'title': 'Dead Poets Society', 'total': 100, 'progress': 0},
        {'title': 'A Perfect World', 'total': 100, 'progress': 0},
        {'title': 'Leon', 'total': 100, 'progress': 0},
        {'title': 'Mahjong', 'total': 100, 'progress': 0},
        {'title': 'Swallowtail Butterfly', 'total': 100, 'progress': 0},
        {'title': 'King of Comedy', 'total': 100, 'progress': 0},
        {'title': 'Devils on the Doorstep', 'total': 100, 'progress': 0},
        {'title': 'WALL-E', 'total': 100, 'progress': 0},
        {'title': 'The Pork of Music', 'total': 100, 'progress': 0},
    ]

    user = User(name=name, username=user_name)
    user.set_password(passwd)
    db.session.add(user)
    for p in projects:
        p['percent'] = "%.2f%%" % round(p['progress']/p['total']*100, 2)
        project = Project(title=p['title'], total=p['total'], progress=p['progress'], percent=p['percent'])
        db.session.add(project)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

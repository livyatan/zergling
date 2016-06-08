import os
import praw
import click
import couchdb


@click.command()
@click.argument('action')
@click.option('--userid', '-u', help='USERID')
def main(action, userid):
    assert action in ('up', 'down')

    db_server = couchdb.client.Server(os.environ['COUCH'])
    db = db_server['zergling']


if __name__ == '__main__':
    main()

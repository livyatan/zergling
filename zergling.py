from __future__ import print_function

import os
# import praw
import click
import couchdb


db = None


@click.command()
@click.argument('action')
@click.option('--thing', '-t', help='THING_URL')
@click.option('--userid', '-u', help='USERID')
def main(action, userid, thing):
    assert action in ('list', 'up', 'down')

    if action == 'list':
        cmd_list()

    if action in ('up', 'down'):
        assert thing is not None
        cmd_vote(action, userid, thing)


def cmd_list():
    for id_ in db:
        print(id_)


def cmd_vote(action, userid, thing):
    print('{} vote {} with user {}'.format(action, thing, userid))
    print('Retrieving zergling')
    zergling = db[userid]


if __name__ == '__main__':
    db_server = couchdb.client.Server(os.environ['COUCH'])
    db = db_server['zergling']

    main()

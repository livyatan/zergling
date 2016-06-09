from __future__ import print_function

import os
import praw
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
    reddit = praw.Reddit(user_agent='deadbeefcafebabe')
    print(zergling['username'])
    print(zergling['ptpwd'])
    try:
        print('Logging in as {}'.format(userid))
        reddit.login(zergling['username'], zergling['ptpwd'],
                     disable_warning=True)
        print('Logging succeeded'.format(userid))
    except praw.errors.InvalidUserPass:
        print('User {} not valid'.format(userid))
        del db[userid]
        print('User {} deleted'.format(userid))
    else:
        submission = reddit.get_submission(thing)
        redditor = reddit.get_redditor(userid)

        if action == 'up':
            submission.upvote()
            print('Upvoted')
            zergling['upvoted'] = zergling.get('upvoted', [])
            zergling['upvoted'].append(thing)
            if thing in set([s.permalink for s in redditor.get_liked()]):
                print('Upvote recorded')
        elif action == 'down':
            submission.downvote()
            print('Downvoted')
            zergling['downvoted'] = zergling.get('downvoted', [])
            zergling['downvoted'].append(thing)
            if thing in set([s.permalink for s in redditor.get_disliked()]):
                print('Downvote recorded')

        db.save(zergling)
        redditor.get_liked


if __name__ == '__main__':
    db_server = couchdb.client.Server(os.environ['COUCH'])
    db = db_server['zergling']

    main()

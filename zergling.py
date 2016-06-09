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


def get_thing(reddit, permalink):
    submission = reddit.get_submission(permalink)
    if submission.permalink == permalink:
        print('The permalink is a submission')
        return submission
    print('The permalink is a comment. Looking for the comment')
    return get_comment(submission.comments, permalink)


def get_comment(comments, permalink):
    for comment in comments:
        if comment.permalink == permalink:
            return comment

        # Find in replies
        reply = get_comment(comment.replies, permalink)
        if reply:
            return reply

    return None


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
        t = get_thing(reddit, thing)

        if action == 'up':
            t.upvote()
            print('Upvoted')
            zergling['upvoted'] = zergling.get('upvoted', [])
            zergling['upvoted'].append(thing)
        elif action == 'down':
            t.downvote()
            print('Downvoted')
            zergling['downvoted'] = zergling.get('downvoted', [])
            zergling['downvoted'].append(thing)

        db.save(zergling)


if __name__ == '__main__':
    db_server = couchdb.client.Server(os.environ['COUCH'])
    db = db_server['zergling']

    main()

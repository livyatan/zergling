from __future__ import print_function

import os
import praw
import click
import couchdb
import uuid


db = None


@click.command()
@click.argument('action')
@click.option('--thing', '-t', help='THING_URL')
@click.option('--userid', '-u', help='USERID')
def main(action, userid, thing):
    assert action in ('list', 'up', 'down', 'clean')

    if action == 'list':
        cmd_list()

    if action == 'clean':
        cmd_clean()

    if action in ('up', 'down'):
        assert thing is not None
        cmd_vote(action, userid, thing)


def create_reddit_client():
    return praw.Reddit(user_agent=uuid.uuid4().hex)


def cmd_list():
    for id_ in db:
        print(id_)


def cmd_clean():
    total_cleaned = 0
    for id_ in db:
        zergling = db[id_]
        print('Validating zergling: {}'.format(id_))
        reddit = create_reddit_client()
        if kill_zergling_if_invalid(reddit, zergling):
            total_cleaned += 1
    print('Total zerglings cleaned: {}'.format(total_cleaned))


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


def kill_zergling_if_invalid(reddit, zergling):
    userid = zergling['username']
    try:
        print('Logging in as {}'.format(userid))
        reddit.login(zergling['username'], zergling['ptpwd'],
                     disable_warning=True)
        print('Logging succeeded'.format(userid))
        return False
    except praw.errors.InvalidUserPass:
        print('User {} not valid'.format(userid))
        del db[userid]
        print('User {} deleted'.format(userid))
        return True


def cmd_vote(action, userid, thing):
    print('{} vote {} with user {}'.format(action, thing, userid))
    print('Retrieving zergling')
    zergling = db[userid]
    reddit = create_reddit_client()
    print(zergling['username'])
    print(zergling['ptpwd'])

    kill_zergling_if_invalid(reddit, zergling)

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

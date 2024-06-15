import subprocess
import os


ADDED_WORDS = "added".split(' ')
CHANGED_WORDS = "updated changed enhanced".split(' ')
REMOVED_WORDS = "removed deleted".split(' ')
NAMES = ['added', 'changed', 'removed', 'unclassified changes']

def get_msg_type(msg):
    msg = msg.lower()

    for w in ADDED_WORDS:
        if w in msg:
            return 'added'

    for w in CHANGED_WORDS:
        if w in msg:
            return 'changed'

    for w in REMOVED_WORDS:
        if w in msg:
            return 'deleted'

    return 'unclassified changes'


def add_changelog_entry(changelog, tag=None):
    changelog.append({'tag': None, 'added': [], 'changed': [], 'removed': [], 'unclassified changes': [], 'date': None})


def main():
    # retrieve current branch name
    branch = [b[2:] for b in subprocess.check_output("git branch".split(' ')).decode('utf-8').split('\n') if b[:2] == '* '][0]
    # retrieve commit history with tags
    out = subprocess.check_output(f"git log {branch} --pretty=format:'%C(auto)%h%d (%ci) %cn <%ce> %s'".split(' ')).decode('utf-8').split('\n')
    commits = [commit_parser(line) for line out]

    # list of versions
    # a version is a dict {'tag': 'xxxxxx', added': [], 'changed': [], 'removed': []}
    changelog = []
    add_changelog_entry(changelog)

    for commit in commits:
        if commit['tag']:
            add_changelog_entry(changelog, commit['tag'])
        p = len(changelog) - 1
        changelog[p][get_msg_type(commit['msg'])] = commit['msg']

    output = "# Changelog\n\n"
    for changes in changelog:
        output += f"## [{'Unreleased changes' if changes['tag'] is None else changes['tag']}] - {changes['date']}\n"

        for t in NAMES:
            output += f"### {t.capitalize()}\n"
            for content in changes[t][::-1]:  # get chronological order
                output += f"- {content}\n"
            output += "\n"

    with open('CHANGELOG.md', 'w') as f:
        f.write(output)


def commit_parser(commit):
    sha = commit[:7]
    commit = commit[8:]

    # find tag if any
    tag = None
    if commit[:4] == "(tag":
        commit = commit[6:]
        tag = ""
        for c in commit:
            if c != ')':
                tag += c
            else:
                break
    commit = commit[len(tag) + 2 if tag is not None else 0:]

    # remove branch if specified
    if commit[:7] == "(origin":
        origin = ""
        for c in commit:
            if c != ')':
                origin += c
            else:
                break
        commit = commit[len(origin) + 2:]

    # find date
    date = ""
    if commit[:2] == "(2":  # it's safe to assume this software will be used only between years 2000 and 2999
        commit = commit[1:]
        for c in commit:
            if c != ")":
                date += c
            else:
                break
    commit = commit[len(date) + 2 if date else 0:]

    # find author
    author = ""
    for c in commit:
        if c != '<':
            author += c
        else:
            break
    commit = commit[len(author) + 1 if author else 0:]
    author = ' '.join(e for e in author.split(' ') if e)  # remove whitespaces at beginning and end if any

    # find author mail
    mail = ""
    for c in commit:
        if c != ">":
            mail += c
        else:
            break
    commit = commit[len(mail) + 2 if mail else 0:]

    # find message
    message = commit
    return {
        'sha': sha,
        'tag': tag,
        'msg': message,
        'date': date[:len(date) - 15],  # get rid of the "hour:min:sec +0200" thing
        'author': {
            'name': author,
            'email': mail
        }
    }


if __name__ == '__main__':
    main()
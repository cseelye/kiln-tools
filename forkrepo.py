#!/usr/bin/env python2.7
"""Delete a repo on Kiln"""

from pyapputil.appframework import PythonApp
from pyapputil.argutil import ArgumentParser
from pyapputil.typeutil import ValidateAndDefault, StrType
from pyapputil.logutil import GetLogger, logargs

from kilnapi import KilnError, find_repo, create_fork, wait_for_repo

@logargs
@ValidateAndDefault({
    # "arg_name" : (arg_type, arg_default)
    "token" : (StrType(), None),
    "parent_name" : (StrType(), None),
    "repo_name" : (StrType(), None)
})
def main(token,
         parent_name,
         repo_name):

    log = GetLogger()

    log.info("Searching for parent repo '{}'".format(parent_name))
    try:
        parent_name, parent_id, repo_group  = find_repo(token, parent_name)
    except KilnError as ex:
        log.error(ex.message)
        return False

    log.info("Creating '{}' as a fork of '{}'".format(repo_name, parent_name))
    try:
        new_repo = create_fork(token, repo_name, parent_id, repo_group)
    except KilnError as ex:
        log.error(ex.message)
        return False

    log.info("Waiting for repo to finish creating on Kiln")
    try:
        wait_for_repo(token, new_repo["ixRepo"])
    except KilnError as ex:
        log.error(ex.message)
        return False

    log.passed("Successfully created new repo")

if __name__ == "__main__":
    parser = ArgumentParser(description="Create a new fork of an existing repo in Kiln")
    parser.add_argument("-t", "--token", type=StrType(), use_appconfig=True, help="Your Kiln/Fogbugz token. If you do not have one, go to your user prefs and create an API token")
    parser.add_argument("parent_name", type=StrType(), help="The name of the parent repo to fork")
    parser.add_argument("repo_name", type=StrType(), help="The name of the new repo to create")
    args = parser.parse_args_to_dict()

    app = PythonApp(main, args)
    app.Run(**args)

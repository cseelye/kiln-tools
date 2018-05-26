#!/usr/bin/env python2.7
"""Delete a repo on Kiln"""

from pyapputil.appframework import PythonApp
from pyapputil.argutil import ArgumentParser
from pyapputil.typeutil import ValidateAndDefault, StrType
from pyapputil.logutil import GetLogger, logargs

from kilnapi import KilnError, delete_repo

@logargs
@ValidateAndDefault({
    # "arg_name" : (arg_type, arg_default)
    "token" : (StrType(), None),
    "repo_name" : (StrType(), None)
})
def main(token,
         repo_name):

    log = GetLogger()

    log.info("Deleting repo '{}'".format(repo_name))
    try:
        delete_repo(token, repo_name)
    except KilnError as ex:
        log.error(ex.message)
        return False
    log.passed("Successfully deleted '{}'".format(repo_name))
    return True

if __name__ == "__main__":
    parser = ArgumentParser(description="Delete a repo in Kiln")
    parser.add_argument("-t", "--token", type=StrType(), use_appconfig=True, help="Your Kiln/Fogbugz token. If you do not have one, go to your user prefs and create an API token")
    parser.add_argument("repo_name", type=StrType(), help="The name of the repo to delete")
    args = parser.parse_args_to_dict()

    app = PythonApp(main, args)
    app.Run(**args)

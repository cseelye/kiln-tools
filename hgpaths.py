#!/usr/bin/env python2.7
"""
Create an hg paths configuration file with all of the repos available in your Kiln instance.

This allows you to use short aliases instead of the full repo path. I typically use this tool to write out an .hgpaths 
file, and then include that file in my main .hgrc
%include ~/.hgpaths
"""

from pyapputil.appframework import PythonApp
from pyapputil.argutil import ArgumentParser
from pyapputil.typeutil import ValidateAndDefault, StrType
from pyapputil.logutil import GetLogger, logargs

from kilnapi import KilnError, api_path, call_api
import os

@logargs
@ValidateAndDefault({
    # "arg_name" : (arg_type, arg_default)
    "token" : (StrType(), None),
    "hgpaths_file" : (StrType(), None)
})
def main(token,
         hgpaths_file):

    log = GetLogger()

    hgpaths_file = os.path.expanduser(hgpaths_file)
    hgpaths_file = os.path.expandvars(hgpaths_file)

    log.info("Getting a list of repos from Kiln")
    try:
        project_list = call_api(api_path("Project"), {"token" : token})
    except KilnError as ex:
        log.error(ex.message)
        return False

    count = 0
    paths = {}
    for proj in project_list:
        if proj["sName"] != "Repositories":
            continue
        for group in proj["repoGroups"]:
            for repo in group["repos"]:
                paths[repo["sName"]] = repo["sHgSshUrl"]
                count += 1

    with open(hgpaths_file, "w") as output:
        output.write("[paths]\n")
        for name in sorted(paths.keys()):
            path = paths[name]
            output.write("{} = {}\n".format(name, path))
            log.info("    {} {}".format(name, path))
        output.flush()

    log.info("Successfully wrote {} repos to {}".format(count, hgpaths_file))
    return True

if __name__ == "__main__":
    parser = ArgumentParser(description="Create an hg paths config file with all of the repos in your Kiln instance. This file can then be %include in your .hgrc file to make hg operations easier")
    parser.add_argument("-t", "--token", type=StrType(), use_appconfig=True, help="Your Kiln/Fogbugz token. If you do not have one, go to your user prefs and create an API token")
    parser.add_argument("-f", "--hgpaths_file", type=StrType(), use_appconfig=True, help="Name of your hgpaths file")
    args = parser.parse_args_to_dict()

    app = PythonApp(main, args)
    app.Run(**args)

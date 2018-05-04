#!/usr/bin/env python2.7
"""Basic interaction with the Kiln API"""
from __future__ import print_function

from pyapputil.appconfig import appconfig
from pyapputil.logutil import GetLogger

import requests
import sys
import time

_log = GetLogger()

if "kiln_url" not in appconfig:
    print("* * Please specify a kiln_url in your userconfig.yml * *")
    sys.exit(1)

class KilnError(Exception):
    """Thrown when there is any kind of error interacting with the Kiln API"""
    pass

def api_path(url):
    """Build a Kiln API path"""
    return "{}/Api/1.0/{}".format(appconfig["kiln_url"], url)

def call_api(url, params=None, post=False):
    """Call a Kiln API method"""
    params = params or {}
    try:
        if post:
            _log.debug("POST {} with params {}".format(url, params))
            handle = requests.post(url, params)
        else:
            _log.debug("GET {} with params {}".format(url, params))
            handle = requests.get(url, params)
        handle.raise_for_status()
    except requests.RequestException as ex:
        raise KilnError(ex.message)

    result = handle.json()
    _log.debug2(result)
    if isinstance(result, bool):
        return result
    if "errors" in result:
        err_message = [err["sError"] for err in result["errors"]]
        raise KilnException("Error: " + ", ".join(err_message))
    return result

def find_repo(token, repo_name):
    """Find an existing repo by name"""
    _log.debug("Searching for repo '{}'".format(repo_name))
    _log.debug2("Getting a list of all projects/repo groups/repos")
    project_list = call_api(api_path("Project"), {"token" : token})
    for proj in project_list:
        for group in proj["repoGroups"]:
            for repo in group["repos"]:
                if repo["sName"] == repo_name:
                    return repo["sName"], repo["ixRepo"], group["ixRepoGroup"]
    raise KilnError("Could not find repo '{}'".format(repo_name))

def create_fork(token, fork_name, parent_id, repo_group_id):
    """Creat a new fork of an existing repo"""
    return call_api(api_path("Repo/Create"), {"token" : token, "sName" : fork_name, "ixParent" : parent_id, "fCentral" : False, "ixRepoGroup" : repo_group_id}, post=True)

def wait_for_repo(token, repo_id):
    """Wait for a repo to be finished creating and ready to use"""
    while True:
        result = call_api(api_path("Repo/{}".format(repo_id)), {"token" : token})
        if result["sStatus"] == "good":
            break
            time.sleep(2)

def delete_repo(token, repo_name):
    """Delete a repo by name"""
    _, repo_id, _ = find_repo(token, repo_name)
    return call_api(api_path("Repo/{}/Delete".format(repo_id)), {"token" : token}, post=True)

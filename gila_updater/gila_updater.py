import json
import re
import subprocess

from git import Repo


class GilaUpdater:

    def __init__(self):
        self.repo_url = "https://github.com/fran-00/gila.git"

    def compare_local_and_remote_sha(self):
        with open('storage/gila_conf.json', 'r') as f:
            data = json.load(f)
        local_sha = data["local_sha"]
        process = subprocess.Popen(["git", "ls-remote", self.repo_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        remote_sha = re.split(r'\t+', stdout.decode('ascii'))[0]
        if local_sha != remote_sha:
            print("Codebase is not updated!")
        else:
            print("Codebase is updated!")

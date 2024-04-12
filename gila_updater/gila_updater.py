import os
import subprocess
import sys

from git import Repo


class GilaUpdater:

    def __init__(self):
        self.repo_url = "https://github.com/fran-00/gila.git"
        self.local_dir = "storage/cloned_repo"

    def install_requirements(self, requirements_file):
        activate_script = os.path.join(
            self.local_dir, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
        try:
            subprocess.run([activate_script, '&&', 'pip', 'install',
                           '-r', requirements_file], shell=False, check=True)
            print("Pacchetti di terze parti installati con successo!")
        except Exception as e:
            print(f"Si è verificato un errore durante l'installazione dei pacchetti di terze parti: {e}")

import os
import shutil
import subprocess
import sys
import venv

from git import Repo


class GilaUpdater:

    def __init__(self):
        self.repo_url = "https://github.com/fran-00/gila.git"
        self.local_dir = "storage/cloned_repo"

    def create_virtualenv(self, env_dir):
        venv.create(env_dir, system_site_packages=False, clear=True)
        print(f"Ambiente virtuale creato con successo in: {env_dir}")

    def install_requirements(self, requirements_file):
        activate_script = os.path.join(
            self.local_dir, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
        try:
            subprocess.run([activate_script, '&&', 'pip', 'install',
                           '-r', requirements_file], shell=False, check=True)
            print("Pacchetti di terze parti installati con successo!")
        except Exception as e:
            print(f"Si è verificato un errore durante l'installazione dei pacchetti di terze parti: {e}")

    def clone_repo(self):
        repo = Repo.clone_from(self.repo_url, self.local_dir)
        env_dir = os.path.join(self.local_dir, 'venv')
        self.create_virtualenv(env_dir)
        requirements_file = os.path.join('/storage/cloned_repo/', 'requirements.txt')
        if os.path.exists(requirements_file):
            self.install_requirements(env_dir, requirements_file)
        try:

            os.chdir(self.local_dir)
            activate_script = os.path.join(
                env_dir, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
            subprocess.run([activate_script, '&&', 'pyinstaller',
                           'build.spec'], shell=True, check=True)
            # shutil.rmtree('build')
            # shutil.rmtree('nome_script.spec')
            print("Build completata con successo!")
        except Exception as e:
            print(f"Si è verificato un errore durante la build: {e}")

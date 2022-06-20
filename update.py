import subprocess
import os
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree

repo_dir = os.path.join(os.getcwd(), 'expensetracker')
current_dir = os.getcwd()
version_check_cmd = "git rev-list --left-right --count origin/master"
repo_clone_cmd = "git clone https://github.com/Prowler1000/expensetracker -b master"
repo_pull_cmd = "git pull https://github.com/Prowler1000/expensetracker"
install_node_modules_cmd = "npm ci"
node_build_cmd = "npm run build"

def run_cmd(cmd, workingdir):
    result = subprocess.run(cmd, cwd=workingdir, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def check_for_updates():
    update_required = not Path(repo_dir).exists()
    if not update_required:
        result = subprocess.run(version_check_cmd, cwd=repo_dir, shell=True, stdout=subprocess.PIPE)
        decoded_result = result.stdout.decode('utf-8').replace('\t', '')
        update_required = not all(not x.isdigit() or x == "0" for x in decoded_result)
    return update_required


def do_update():
    if not Path(repo_dir).exists():
        run_cmd(repo_clone_cmd, current_dir)
    else:
        run_cmd(repo_pull_cmd, cwd=repo_dir)
    run_cmd(install_node_modules_cmd, repo_dir)
    run_cmd(node_build_cmd, repo_dir)
    shutil.copy(os.path.join(repo_dir, "next.config.js"), "./next.config.js")
    shutil.copytree(os.path.join(repo_dir, "public"), "./public")
    shutil.copy(os.path.join(repo_dir, "package.json"), "./package.json")
    copy_tree(os.path.join(repo_dir, ".next", "standalone"), "./")
    shutil.copytree(os.path.join(repo_dir, ".next", "static"), os.path.join(os.getcwd(), ".next", "static"))
    

need_update = check_for_updates()
if (need_update): do_update()
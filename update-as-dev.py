import subprocess
import os
import shutil
import sys
from pathlib import Path
from distutils.dir_util import copy_tree

server_folder_name = sys.argv[1]

current_dir = os.getcwd()
repo_dir = os.path.join(current_dir, 'dev-repo')
server_dir = os.path.join(current_dir, server_folder_name)

fetch_cmd = "git fetch"
version_check_cmd = "git rev-list --left-right --count origin/master..."
repo_clone_cmd = "git clone https://github.com/Prowler1000/expensetracker -b dev ./repo"
repo_pull_cmd = "git pull origin master -f"
install_node_modules_cmd = "npm ci"
node_build_cmd = "npm run build"

nextjsconfig_src = os.path.join(repo_dir, "next.config.js")
nextjsconfig_dst = os.path.join(server_dir, "./next.config.js")

public_src = os.path.join(repo_dir, "public")
public_dst = os.path.join(server_dir, "./public")

packagejson_src = os.path.join(repo_dir, "package.json")
packagejson_dst = os.path.join(server_dir, "./package.json")

standalone_src = os.path.join(repo_dir, ".next", "standalone")
standalone_dst = os.path.join(server_dir)

nextstatic_src = os.path.join(repo_dir, ".next", "static")
nextstatic_dst = os.path.join(server_dir, ".next", "static")

def run_cmd(cmd, workingdir):
    result = subprocess.run(cmd, cwd=workingdir, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def check_for_updates():
    update_required = not Path(repo_dir).exists()
    if not update_required:
        run_cmd(fetch_cmd, repo_dir)
        result = run_cmd(version_check_cmd, repo_dir)
        update_required = not all(not x.isdigit() or x == "0" for x in result)
    return update_required


def do_update():
    if not Path(repo_dir).exists():
        run_cmd(repo_clone_cmd, current_dir)
    else:
        run_cmd(repo_pull_cmd, repo_dir)
    run_cmd(install_node_modules_cmd, repo_dir)
    run_cmd(node_build_cmd, repo_dir)
    copy_files()

    
def copy_files():
    if Path(server_dir).exists():
        shutil.rmtree(server_dir)
    os.mkdir(server_dir)
    shutil.copy(nextjsconfig_src, nextjsconfig_dst)
    shutil.copy(packagejson_src, packagejson_dst)
    copy_tree(nextstatic_src, nextstatic_dst)
    copy_tree(public_src, public_dst)
    copy_tree(standalone_src, standalone_dst)
    
    
need_update = check_for_updates()
if (need_update): do_update()
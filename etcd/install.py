#!/usr/bin/env python

import subprocess
import os
import errno
import shutil
import tempfile


def run_command(args, stdin='', exit_codes=[0], cwd=None, **kwargs):
  print "Running command: " + ' '.join(args)

  proc = subprocess.Popen(args,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          cwd=cwd,
                          **kwargs)

  out, err = proc.communicate(input=stdin)
  retcode = proc.returncode
  if not retcode in exit_codes:
    print "Calling return error: " + ' '.join(args)
    print "Output: " + out
    print "Error: " + err
    raise subprocess.CalledProcessError(retcode, args)
  return out, err

def create_dir(path, mode, owner, group):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

    cmd = ['chmod', mode, path]
    run_command(cmd)

    cmd = ['chown', owner + ':' + group, path]
    run_command(cmd)

def create_user(name):
	cmd = ['adduser', '--system', '--no-create-home', '--group', name]
	run_command(cmd)


def clone_source(repo):
	destdir = tempfile.mkdtemp()
	print "Cloning %s into %s" % (repo, destdir)
	cmd = ['git', 'clone', repo, destdir]
	run_command(cmd)
	return destdir

def copy_file(src, dst):
	shutil.copyfile(src, dst)

def create_service(name):
	src = name + '.service'
	dst = '/lib/systemd/system/' + name + '.service'
	shutil.copyfile(src, dst)
	run_command(['systemctl', 'enable', name + '.service'])
	run_command(['systemctl', 'start', name + '.service'])

create_user('etcd')

create_dir('/var/lib/etcd', '0755', 'etcd', 'etcd')
create_dir('/var/run/etcd', '0755', 'etcd', 'etcd')

etcd = clone_source('https://github.com/coreos/etcd.git')
run_command([os.path.join(etcd, 'build')], cwd=etcd)
copy_file(os.path.join(etcd, 'bin/etcd'), '/usr/bin/etcd')

create_service('etcd')

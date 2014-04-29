#!/usr/bin/env python

from pinstall.direct import *

create_group('etcd')
create_user('etcd')

create_dir('/var/lib/etcd', '0755', 'etcd', 'etcd')
create_dir('/var/run/etcd', '0755', 'etcd', 'etcd')

etcd = clone_source('https://github.com/coreos/etcd.git')
run_command([os.path.join(etcd, 'build')], cwd=etcd)
copy_file(os.path.join(etcd, 'bin/etcd'), '/usr/bin/etcd', '0755', 'root', 'root')

create_service('etcd')


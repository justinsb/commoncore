#!/usr/bin/env python

from pinstall.direct import *

src = clone_source('https://github.com/coreos/fleet.git')
run_command([os.path.join(src, 'build')], cwd=src)
copy_file(os.path.join(src, 'bin/fleet'), '/usr/bin/fleet', '0755', 'root', 'root')
copy_file(os.path.join(src, 'bin/fleetctl'), '/usr/bin/fleetctl', '0755', 'root', 'root')

create_service('fleet')


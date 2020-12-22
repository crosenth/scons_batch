"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import SCons


class Environment(SCons.Environment.Environment):
    def __init__(self,
                 script_dir='bin',
                 cpus=None,
                 memory=None,
                 jobDefinition=None,
                 queue=None,
                 bucket=None,
                 verbosity=0,
                 **kwargs):
        self.bucket = bucket
        self.cpus = cpus
        self.jobDefinition = jobDefinition
        self.memory = memory
        self.queue = queue
        if os.path.isdir(script_dir):
            self.script_dir = script_dir
            self.scripts = os.listdir(script_dir)
        else:
            self.script_dir = None
            self.scripts = []
        self.verbosity = verbosity
        SCons.Environment.Environment.__init__(self, **kwargs)

    def Command(self,
                target,
                source,
                action,
                cpus=None,
                memory=None,
                jobDefinition=None,
                queue=None,
                bucket=None,
                verbosity=1,
                **kw):
        bucket = bucket or self.bucket
        cpus = cpus or self.cpus
        jobDefinition = jobDefinition or self.jobDefinition
        memory = memory or self.memory
        queue = queue or self.queue
        verbosity = verbosity or self.verbosity
        if not jobDefinition:
            raise ValueError('jobDefinition must be defined')
        if not queue:
            raise ValueError('queue must be defined')
        if isinstance(action, str):
            action = [action]
        batch_actions = []
        for a in action:
            if not isinstance(a, str):
                raise ValueError('Batch not supported for ' + str(a))
            batch = ['aws_batch', '--job-queue', queue]
            if bucket:
                batch.extend(['--bucket', bucket])
            if cpus:
                batch.extend(['--cpus', cpus])
            if memory:
                batch.extend(['--memory', memory])
            uploads = []
            script = a.split()[0]
            if script in self.scripts:
                script = os.path.join(self.script_dir, script)
                uploads.append(script)
                self.Depends(target, script)
                command = 'PATH=$$PATH:{}; {}'.format(self.script_dir, a)
            else:
                command = a
            batch.extend(['--command', '"{}"'.format(command)])
            if source:
                if isinstance(source, list):
                    uploads.extend(source)
                else:
                    uploads.append(source)
            if uploads:
                batch.extend(['--uploads', ','.join(uploads)])
            if target:
                if isinstance(target, list):
                    target = ','.join(target)
                batch.extend(['--downloads', target])
            if verbosity:
                batch.append('-' + 'v' * verbosity)
            batch.append(jobDefinition)
            batch = (str(i) for i in batch)
            batch_actions.append(_BatchAction(a, ' '.join(batch), verbosity))
        return SCons.Environment.Environment.Command(
            self, target, source, batch_actions, **kw)


class _BatchAction(SCons.Action.CommandAction):
    def __init__(self, command, batch, verbosity, **kw):
        self.command = batch if verbosity else command
        SCons.Action.CommandAction.__init__(self, batch, **kw)

    def print_cmd_line(self, _, target, source, env):
        c = env.subst(self.command, SCons.Subst.SUBST_RAW, target, source)
        SCons.Action.CommandAction.print_cmd_line(self, c, target, source, env)

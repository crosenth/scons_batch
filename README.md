# AWS Batch SCons plugin

Allows users to execute SCons Actions using AWS Batch

## dependencies

* Python 3.x

As described in setup.py:

* aws_batch>=0.6
* scons>=3.1.1

The awscli must also be available within the batch container.

## installation

```
% pip install git+https://github.com/crosenth/scons_batch
```

## Usage

Scons Batch extends the SCons.SCons.Environment class so all the regular
environment constructor values can be passed in addition to the 
aws_batch.Environment constructor values.

```
import scons_batch

env = scons_batch.Environment(
    bucket='s3://my_bucket/',
    cpu=2,
    jobDefinition='some_job_definition',
    memory=1028,
    queue='some_queue',
    script_dir='bin',  # where any custom scripts live
    verbosity=0
    )

hello = env.Command(
   target='hello_world.txt',
   source=None,
   action='echo hello world > $TARGET')
```

None of the values are required but both the queue and jobDefinition arguments
must be defined at least at the Command level.  All arguments can be specified
or overridden at the Command level.  The verbosity argument is set
to 0 by default which will hide the full aws_batch action.

```
scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
echo hello world > output/hello_world.txt
scons: done building targets.
```

With `verbosity=1`:

```
scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
aws_batch --job-queue some-queue --bucket s3://my_bucket/ --command "cat hello world > hello_world.txt" --downloads hello_world.txt -v some_job_definition
Found credentials in shared credentials file: ~/.aws/credentials
mkdir -p tmp; cd tmp; cat hello world > hello_world.txt; /home/ec2-user/miniconda/bin/aws s3 cp --only-show-errors hello_world.txt s3://my_bucket/hello_world.txt
SUBMITTED
RUNNABLE
STARTING
SUCCEEDED
download: s3://my_bucket/hello_world.txt to hello_world.txt
scons: done building targets.
```

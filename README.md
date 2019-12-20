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
import aws_batch

env = aws_batch.Environment(
    bucket='s3://my_bucket/',
    cpu=2,
    jobDefinition='some_job_definition',
    memory=1028,
    queue='some_queue',
    script_dir='bin',  # where any custom scripts live
    verbosity=0
    )
```

None of the values are required but both the queue and jobDefinition arguments
must be passed at least at the Command level.  The verbosity argument is set
to 0 by default which will hide the full aws_batch action.

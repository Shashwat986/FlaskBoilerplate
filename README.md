# Flask API Server Setup

This repository contains a set of examples for multiple functions required in a Flask API server. I'll be going through each of these examples, and how they are structured below.

## Overall Structure

- `app/config.py`: This is the configuration file used by Flask
- `app/controllers`: This is where we have all the controllers
- `app/helpers`: This folder contains all the helpers. Helpers will contain code that perform specific functions, that is modularized so that our controllers remain skinny
- `app/models`: This folder contains all our models.
- `app/workers`
- `pytest.ini`: This is the configuration file used by `pytest`
- `redis.conf`: This is the configuration file used by `redis-server`
- `requirements.txt`: All the modules required by this repository
- `run.py`: This file needs to be run to start the API Server
- `seed.py`: An example seed file that interacts with the SQLite Database
- `supervisord.conf`: This is the configuration file used by `supervisor`
- `test/`: This directory contains all the test files. These test files are executed using `pytest`

### Supervisor

[Supervisor](http://supervisord.org/index.html) is a process manager. It allows us to run processes in the background. It monitors these processes and ensures that they remain up.

The config file in thie repository also starts an inet HTTP server that will be found at [127.0.0.1:9001](http://127.0.0.1:9001) and allows us to monitor the status of each of the programs defined in the config file.

We have 3 programs configured in this file:

1. `main`: This is the main Flask app server.
1. `redis`: This is a locally-hosted redis server, run using the default command of `redis-server` with an associated config file `redis.conf`.
1. `worker`: This spawns 2 workers. Each worker is an instance of [RQ](#rq-job-scheduler), which allows us to schedule background jobs.

We can add anything else that we want to run in the same server instance out here, to ensure that all processes run all the time.

### RQ Job Scheduler

[RQ](https://python-rq.org/) is a scheduler that uses redis queues to enqueue and dequeue jobs. Workers should be used to perform any async task. We can also use RQ to schedule tasks for later, or retry certain tasks at some particular time in the future. We can also schedule tasks at different priority levels to ensure important tasks do not get delayed.

To monitor the workers and tasks being processed, we can head to a dashboard provided by [rq-dashboard](https://github.com/Parallels/rq-dashboard) and hosted at [/internal/rq](http://127.0.0.1:5000/internal/rq).

An example of a job being scheduled within a controller can be found at `app/controllers/baz.py`.

### SQLAlchemy, `app/models`, and mixins

To better structure the database tables, the `app/models` folder will contain one file for each table. This folder will be used exclusively for DB tables. If we have any other self-contained models, we can put them in the `app/services` folder (to be added).

We are also using [SQLAlchemy](https://docs.sqlalchemy.org/en/13/) as an ORM to allow us to fetch objects in an easy, friendly manner, and, along with SQLAlchemy, we are using [SQLAlchemy mixins](https://github.com/absent1706/sqlalchemy-mixins) to give us many more helper functions to better query the database.

SQLAlchemy is configured through `app/config.py`. There's also a helpful `seed.py` file that contains a few examples to demonstrate usage of the ORM and the mixins.

Note: The version of SQLAlchemy mixins that I have used here has a bug where it doesn't commit the record to the database. To fix that, I have overridden the `save()` and `delete()` methods in the `app/models/__init__.py` file. This also has a base class that inherits from `db.Model` and incorporates the mixins, to make the actual model files much cleaner.

### Honeybadger

I have integrated [Honeybadger](https://docs.honeybadger.io/lib/python.html) to catch and report errors in our codebase. The API Key for Honeybadger is set in `app/config.py`. All errors will be reported to Honeybadger and associated alerts can be built to ensure that all failures are known to us, and nothing fails silently.

There are two separate places where a Honeybadger notification can be seen:
- `app/controllers/fail.py` has an API endpoint that will throw a `KeyError`, which will be logged in Honeybadger.
- `app/controllers/foo.py` has an instance of `honeybadger.notify` which is used to throw a custom notification.

### JSON Schema Validation

TBC

### PyTest

TBC

### API Versioning

TBC

### Other Examples

TBC

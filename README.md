# Flask API Server Setup

This repository contains a set of examples for multiple functions required in a Flask API server. I'll be going through each of these examples, and how they are structured below.

## Overall Structure

- `app`
  - `__init__.py`: This file initializes the Flask instance, and creates all instances that need to be accessible elsewhere: `db`, `redis_client`, and `rq`. This also registers blueprints generated in `controllers/__init__.py`.
  - `config.py`: This is the configuration file used while initialising Flask.
  - `controllers`:
    - `__init__.py`: This file creates the Blueprint that is fetched from `app/__init__.py` to be registered.
    - ...: This is where we have all the controllers
  - `helpers`
    - ...: This is where we have our helpers. Helpers will contain code that perform specific functions, that is modularized so that our controllers remain skinny.
  - `models`
    - `__init__.py`: This init file defines `SQLBase`, which is our base class for all SQLAlchemy models.
    - ...: This folder contains all our models.
  - `services`
    - ...: This folder will contain all self-contained services. This is generally where we will put any third-party interactions and logic
  - `workers`
    - ...: This folder contains all our workers
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

One core part of any API platform will be to ensure that request validation happens properly. This is handled using [JSON Schema](https://json-schema.org/).

To take care of validation, a helper function has been created in `app/helpers/validate.py` which takes a schema as input and validates `request.get_json()` against that schema. It also has some code written to call the `<method>_schema_validation_error()` method of the API class whenever a validation failure happens, allowing all the business logic to be at the controller. If `<method>_schema_validation_error()` doesn't exist, it will raise an exception, which will trigger an HTTP 500: Internal Server Error.

An example of using JSON Schema for validation is in the `app/controllers/bar.py` file. Here, if the input validation fails, the helper calls `Bar.post_schema_validation_error`, which then passes on the error in the response.

### PyTest

The test methods in the `test/` directory aren't written in the way they should be. Right now, they assume that the server is up at `localhost:5000` and use `requests` to make API calls to that server with valid and invalid requests. It does the job, but the test module requires the development server to be up and running, and connected to the development database, which isn't ideal from a unit-testing standpoint.

However, it does the job, and adds coverage to the various API endpoints, which is sufficient for now.

### API Versioning

There are multiple ways to perform API versioning. My personal preference is to use the approach suggested in [this Stackoverflow question](https://stackoverflow.com/a/28797512/967478). This approach is pretty self-explanatory. The only concern I have with it is that it invariably leads to code duplication. Duplication doesn't matter too much, because the older versions are expected to be legacy versions, but it can still lead to issues with business logic and maintainence.

In this repository, I have gone for a different way of doing API versioning, where I pass the version code to each route via a route variable, and leave the business logic of API versioning at an individual controller level. This is potentially cleaner from the point of view of code-reuse, and definitely cleaner if each API is separately versioned, but if the entire API platform is versioned every time, this approach may be suboptimal.

An example of this API versioning example may be seen in the `app/controllers/foo.py` which uses the version. The routing logic is available in `app/controllers/__init__.py`.

### Other Examples

#### Caching

There is a very rudimentary example of caching in `app/controllers/baz.py`. The controller just looks at the Redis cache, sees if there's an entry, and if there is, returns it. If there isn't it creates an entry and returns it.

Note: this is a very bad proof of concept, because the code at `app/helpers/redis.py`, which actually does the caching doesn't look at any request parameters or request body before checking and retrieving from the cache. It also expires the cache every 60 seconds. In any real scenario, all of this will need to be changed.

#### Cat Facts

I've created one example service which hits a fun little [Cat Facts API](https://cat-fact.herokuapp.com/) and returns the first cat fact that it finds.

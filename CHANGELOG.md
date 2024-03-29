# Changelog

All notable changes to this project will be documented in this file.

## 0.7.14 (2023-03-21)

### Bug fixes

- fix: can't find version file

## 0.7.13 (2023-03-09)

### Features

- wait n seconds before firing new command to knotd
- support SRV record
- broker health check

### Bug fixes

- Werkzeug failed to load JSON data

## 0.7.12 (2022-04-13)

- Fix: markupsafe > 2.0.1 breaks flask by removing json function
- Fix: non-existing SOA record cause error
- Fix: agent failed to communicate with Knot

## 0.7.12 (2022-04-13)

- Fix: markupsafe > 2.0.1 breaks flask by removing json function
- Fix: non-existing SOA record cause error
- Fix: agent failed to communicate with Knot

## 0.7.11 (2021-10-07)

- Update: removed unused config for CLI app setup. Now the agent is
  used commonly via docker image.
- Update: refactor to have less code. To have a minimal step to call
  libknot directly.

## 0.7.9 - 0.7.10 (2021-09-15)

- Fix: ubuntu-16.04 runner doesn\'t exists anymore
- Fix: github action regression

## 0.7.8 (2021-09-15)

- Add: request knot to block any future operation until the current
  one finished
- Add: retry on socket connection failure
- Update: use libknot from pypi instead
- Update: use venv in docker build
- Update: third-party dependencies
- Update: adjust agent to new libknot structure

## 0.7.7 (2021-05-12)

- Add: support for multiple Kafka broker and multiple Zookeeper

## 0.7.6 (2020-02-15)

- Add: Reject CNAME with root as owner
- Remove: TXT rdata 255 char validation. Knot will handle the split
  automatically

## 0.7.4 (2020-05-19)

- Add: set timezone in the container

## 0.7.3 (2020-05-14)

- Add: check SOA serial limit before any operation
- Fix: reset serial counter if day changed

## 0.7.2 (2020-05-13)

- Fix: allow zone change if day changed

## 0.7.1 (2020-03-22)

- Fix: include TTL as a component of a zone change

## 0.7.0 (2020-03-17)

- Fix timestamp in the database by using UTC0 instead of local time.
- Add Knot clash course documentation
  <https://biznetgio.github.io/guide/knot-clash-course/>.
- Add [remove zone]{.title-ref} endpoint.
- Change authentication method to [basic auth]{.title-ref}.
- Add deployment guide
  <https://restknot.readthedocs.io/en/latest/deploy.html>.
- Add web API docs
  <https://restknot.readthedocs.io/en/latest/restapi.html>.
- Simplify RESTKNOT agent message structure, so that it doesn\'t need
  complicated parser and bouncing back-and-forth message generator
- Remove useless retry in database operation.
- Fix [get single data]{.title-ref} by returning only one
  [dictionary]{.title-ref} instead of a [list]{.title-ref}.
- Fix domain deletion by using Knot [unset]{.title-ref},
  [purge]{.title-ref} didn\'t work as expected.
- Fix different SOA serial values in the Knot record and database.
- Add handling for non-existing data in the [get_one]{.title-ref}
  model.
- Drop column length in the database, since it doesn\'t add any value.
- Fix row arrangement in model insert and update, causing data can\'t
  be inserted into the database.
- Add a step to remove psycopg2-binary dependencies after the build to
  minimize docker image size.
- Add import existing data to the docs
  <https://restknot.readthedocs.io/en/latest/knotintro.html##importing-existing-zones>.
- Add a fallback method to specified [servers.yml]{.title-ref} if
  it\'s not set.
- Add how-to run locally with docker
  <https://restknot.readthedocs.io/en/latest/project/contributing.html##runing-the-project-locally>.
- Add RESTKnot and Knot config, and ansible-playbook example
  <https://restknot.readthedocs.io/en/latest/deploy.html##prepare-application-configs>
- Fix None value being consumed by JSON [dumps]{.title-ref} in
  RESTKnot agent.
- Add space and double quotes escaping in TXT rdata.
- Prevent non-printable char in TXT rdata.
- Add a way to reject the unsupported record type.
- Prevent empty value in RDATA.
- Add a new logger for RESTKnot API and agent.
- Add a way to check producer existence before any operation.
- Add validator to prevent duplicate records and possible duplicate
  records while editing.
- Add validator to prevent [owner]{.title-ref} data containing
  parenthesis.
- Fix [gunicorn]{.title-ref} worker time out by using asynchronous
  send in Kafka and closing it after usage.
- Add [get user by email]{.title-ref} params in the endpoint.
- Add [list zones owned by specific user]{.title-ref} endpoint.
- Add a new logger for success and failure in RESTKnot agent.
- Modify [TTL]{.title-ref} endpoint behavior by using TTL value as an
  input instead of id.
- Add prevention for the agent to exit when a connection to Knot
  socket timed out.
- Add prevention for a user to add multiple records with the same
  RDATA.
- Add the ability to add, delete, and edit a specific record.
- Fix default record creation by creating it one-by-one. Creating them
  all at once causing them can\'t be removed or edited specifically.
- Add DNS rules (CNAME, A, AAAA, SOA, NS, MX, TXT).
- Add more RDATA validation (SOA, OWNER, TXT, MX).
- Add unit tests ([helpers]{.title-ref}, [validators]{.title-ref}).
- Add integration tests (user, record, domain, command, duplicate
  record and email, DNS rules, messages).
- Add a functional test.
- Store node hostname in a static file instead of the database.
- Fix HTTP code status return for the corresponding event.
- Reject zone changes if the maximum limit reached in a day.
- Automatically delegate command on domain creation and deletion.
- Use distributed asynchronous architecture (event-driven).
- Create default SOA, NS, and CNAME record when creating a domain.
- Refactor unused code and files, requirements and unnecessary logic
  or step.

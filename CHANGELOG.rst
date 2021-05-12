Unreleased
==========

0.7.7 (2021-05-12)
==================

- Add: support for multiple Kafka broker and multiple Zookeeper

0.7.6 (2020-02-15)
==================

- Add: Reject CNAME with root as owner
- Remove: TXT rdata 255 char validation. Knot will handle the split automatically

0.7.4 (2020-05-19)
==================

- Add: set timezone in the container

0.7.3 (2020-05-14)
==================

- Add: check SOA serial limit before any operation
- Fix: reset serial counter if day changed

0.7.2 (2020-05-13)
==================

- Fix: allow zone change if day changed

0.7.1 (2020-03-22)
==================

- Fix: include TTL as a component of a zone change

0.7.0 (2020-03-17)
==================

- Fix timestamp in the database by using UTC0 instead of local time.
- Add Knot clash course documentation https://biznetgio.github.io/guide/knot-clash-course/.
- Add `remove zone` endpoint.
- Change authentication method to `basic auth`.
- Add deployment guide https://restknot.readthedocs.io/en/latest/deploy.html.
- Add web API docs https://restknot.readthedocs.io/en/latest/restapi.html.
- Simplify RESTKNOT agent message structure, so that it doesn't need complicated parser and bouncing back-and-forth message generator
- Remove useless retry in database operation.
- Fix `get single data` by returning only one `dictionary` instead of a `list`.
- Fix domain deletion by using Knot `unset`, `purge` didn't work as expected.
- Fix different SOA serial values in the Knot record and database.
- Add handling for non-existing data in the `get_one` model.
- Drop column length in the database, since it doesn't add any value.
- Fix row arrangement in model insert and update, causing data can't be inserted into the database.  
- Add a step to remove psycopg2-binary dependencies after the build to minimize docker image size.
- Add import existing data to the docs https://restknot.readthedocs.io/en/latest/knotintro.html#importing-existing-zones.
- Add a fallback method to specified `servers.yml` if it's not set.
- Add how-to run locally with docker https://restknot.readthedocs.io/en/latest/project/contributing.html#runing-the-project-locally.
- Add RESTKnot and Knot config, and ansible-playbook example https://restknot.readthedocs.io/en/latest/deploy.html#prepare-application-configs
- Fix None value being consumed by JSON `dumps` in RESTKnot agent.
- Add space and double quotes escaping in TXT rdata.
- Prevent non-printable char in TXT rdata.
- Add a way to reject the unsupported record type.
- Prevent empty value in RDATA.
- Add a new logger for RESTKnot API and agent.
- Add a way to check producer existence before any operation.
- Add validator to prevent duplicate records and possible duplicate records while editing.
- Add validator to prevent `owner` data containing parenthesis.
- Fix `gunicorn` worker time out by using asynchronous send in Kafka and closing it after usage.
- Add `get user by email` params in the endpoint.
- Add `list zones owned by specific user` endpoint.
- Add a new logger for success and failure in RESTKnot agent.
- Modify `TTL` endpoint behavior by using TTL value as an input instead of id.
- Add prevention for the agent to exit when a connection to Knot socket timed out.
- Add prevention for a user to add multiple records with the same RDATA.
- Add the ability to add, delete, and edit a specific record.
- Fix default record creation by creating it one-by-one. Creating them all at
  once causing them can't be removed or edited specifically.
- Add DNS rules (CNAME, A, AAAA, SOA, NS, MX, TXT).
- Add more RDATA validation (SOA, OWNER, TXT, MX).
- Add unit tests (`helpers`, `validators`).
- Add integration tests (user, record, domain, command, duplicate record and email, DNS rules, messages).
- Add a functional test.
- Store node hostname in a static file instead of the database.
- Fix HTTP code status return for the corresponding event.
- Reject zone changes if the maximum limit reached in a day.
- Automatically delegate command on domain creation and deletion.
- Use distributed asynchronous architecture (event-driven).
- Create default SOA, NS, and CNAME record when creating a domain.
- Refactor unused code and files, requirements and unnecessary logic or step.

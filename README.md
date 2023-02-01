<div align="center">

<img src='docs/img/resknot-banner.svg' width=150px />

<br/>

<a href="https://github.com/BiznetGIO/RESTKnot/actions/workflows/ci_api.yml">
    <img src="https://github.com/BiznetGIO/RESTKnot/actions/workflows/ci_api.yml/badge.svg" alt="Build status" />
  </a>

</div>

---

Manage DNS records with asynchronous and simple APIs.

RESTKnot provide a high-level asynchronous API to existing Knot DNS
server. This project consists of three applications: RESTKnot agent,
RESTKnot API, and RESTKnot CLI. A user can create DNS record through web
API provided by RESTKnot API, or as command line app using RESTKnot CLI.
Both of them send command to RESTKnot agent which will be translated
into Knot DNS action.

## Features

-   Asynchronous operation
-   Created default DNS records when adding new zone.
-   Untangle all related record when deleting zone with single API.
-   Prevent wrong RDATA format with validation support.
-   Prevent record lost by checking RDATA contents before adding any
    record.

## Take the tour

### Create New Zone

``` bash
curl -X POST \
  http://localhost:5000/api/domain/add \
  -H 'X-API-key: 123' \
  -F user_id=001 \
  -F zone=example.com
```

### Edit a Single Record

``` bash
curl -X PUT \
  http://127.0.0.1:5000/api/record/edit/10 \
  -H 'x-api-key: 123' \
  -F zone=bar.com \
  -F owner=@ \
  -F rtype=NS \
  -F rdata=one.exampledns.com. \
  -F ttl=3600
```

### Delete a Zone

``` bash
curl -X DELETE \
  http://localhost:5000/api/domain/delete \
  -H 'X-API-Key: 123' \
  -F zone=example.com
```

## Project information

-   [Documentation](https://restknot.readthedocs.io/en/stable/index.html)
-   [Contributing](https://restknot.readthedocs.io/en/stable/project/contributing.html)
-   [Changelog](https://restknot.readthedocs.io/en/stable/project/changelog.html)
-   [License](https://restknot.readthedocs.io/en/stable/project/license.html)

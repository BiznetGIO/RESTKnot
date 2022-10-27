# Guide

```shell
$ pip install -r requirements.txt

$ locust --locustfile create_user.py --users 10 --spawn-rate 1 --host http://127.0.0.1:5000/api
$ # Go to http://0.0.0.0:8089, press start, and see the `chart` section. 
$ # Export the chart to png using the `export` button.
```

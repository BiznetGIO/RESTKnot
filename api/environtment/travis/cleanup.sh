#!/bin/bash
cd api
kill -9 `cat save_pid.txt`
rm save_pid.txt
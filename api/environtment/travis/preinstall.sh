#!/bin/bash
psql -c 'create database knotdb;' -U postgres
psql knotdb < api/environtment/travis/db.sql

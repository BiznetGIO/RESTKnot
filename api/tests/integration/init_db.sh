# need to copy schema.sql to current directory.
# Cockroach cli always failed to parse parent directory.
cockroach start --insecure --host=localhost --background
cockroach sql --insecure --host=localhost --execute="CREATE DATABASE knotdb"
cockroach sql --insecure --host=localhost --database=knotdb < ./schema.sql 

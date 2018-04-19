
# requirement(dependency)
Python 2.7.3 or above

# To get your first aid
python main.py -h

# to convert one data dump log(file)
python main.py -f [logfile]

# to convert a group of files under one directory
python main.py -d [dirfile]



# Verify. The output (*.sql files) should be found in the same directory of your program
## wac_wrk_check_list.sql
## wac_test_rule.sql
## wac_test_rule_stats.sql




# To populate data into your Postgres (you need access to DB-Schema)
```
1. copy your sql files into a top-level folder (easier for psql command console):

2. enter psql console by "pgadmin[menu] -> plugins"

3. Move to your psql's local path to somewhere
# \cd G:  [or whatever your local drive volume name]

4. you might check your sql file are there or not?!
# \! dir

5. # \i wac_wrk_check_list.sql
   \i wac_test_rule.sql
   \i wac_test_rule_stats.sql

6. check you have the function available.
   # \sf waca.generate_wac_wrk_check_ext

7. run the function to populate new data into waca.wac_wrk_check_ext
   # select waca.generate_wac_wrk_check_ext()

Done
```
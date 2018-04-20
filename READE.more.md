READE.more.md

## To run all the unit test:(if you are using py2.7)
virtualenv env
source env/bin/activate
pip install pytest

## Then run the test you want:
pytest -k 'extract' -x [all test cases contain keyword extract will be run]

pytest -v [all test cases contain keyword extract will be run]


## or you want to test integration stuff or interested to understand what each module does
You could run each file as a part of building an integration test, or just for reminding what each function does.
 ( No such example code for extract_fields.py )
```
python extract_lines.py

python calc_process.py -t extract_context 
(this will run a function called ctest_extract_context, showing an integrated process based on extract_context )

python calc_process.py -t main_handler
(likewise)

python main.py -f testdata/sample.log.gz

python main.py -f testdata/long_sample.unl.gz

```



 
                     main_handler()

+------------------------------------------------------------------------------------------------------------------------+
| +---------------+               +---------------------------------------+     +-----------------------+                |
| |               |               |                                       |     |                       |                |
| |               |               |    wac_wrk_check_list (append method) +---> | extract_metrics       |                |
| | extract_blocks+--+----------->+                                       |     |                       |                |
| |               |  |            |                                       |     |                       |                |
| +---------------+  |            +---------------------------------------+     +-----------------------+                |
|                    |                                                                                                   |
|                    |      +--------------------------+                                                                 |
|                    |      |                          |                                                                 |
|                    +--->  |    extract_context       |                                                                 |
|                           |                          |                                                                 |
|                           +------------+-------------+                                                                 |
|                                        |                                                                               |
|                                        |                                                                               |
|                           +------------v-------------+  +---------------------------------------------------------+    |
|                           |                          |  |                                                         |    |
|                           |                          |  |   +------------------------------------------+          |    |
|                           |   extract_test_reg_block |  |   |                                          |          |    |
|                           |                          |  |   |                                          |          |    |
|                           +-----------------+--------+  |   |extract_context_regtest_block             |          |    |
|                                             |           |   |extract_context_regtest_title             |          |    |
|                                             |           |   |extract_context_regtest_title_regver      |          |    |
|                                             |           |   |                                          |          |    |
|                                             |           |   +------------------------------------------+          |    |
|                                             |           |                                                         |    |
|                                             |           |                                                         |    |
|                                             |           |                                                         |    |
|                                             |           |   +--------------------------------------+              |    |
|                                             |           |   | extract_context_testblock            |              |    |
|                                             |           |   | extract_context_testblock_rule_recognizer           |    |
|                                             |           |   |                                      |              |    |
|                                             |           |   |                                      |              |    |
|                                             +---------> |   |                                      |              |    |
|                                                         |   +--------------------------------------+              |    |
|                                                         |   +--------------------------------------+              |    |
|                                                         |   |                                      |              |    |
|                                                         |   |extract_context_testblock_rulestat    |              |    |
|                                                         |   |extract_context_testblock_rulestat_error             |    |
|                                                         |   |extract_context_testblock_rulestat_cognition         |    |
|                                                         |   |                                      |              |    |
|                                                         |   +--------------------------------------+              |    |
|                                                         |                                                         |    |
|                                                         +---------------------------------------------------------+    |
|                                                                                                                        |
+------------------------------------------------------------------------------------------------------------------------+

set termout on
spool apply.log
prompt Starting execution of Scripts/test (1).sql
@@"create/Scripts/test (1).sql"
prompt Finished execution of Scripts/test (1).sql
prompt Starting execution of Scripts/test (3).sql
@@"create/Scripts/test (3).sql"
prompt Finished execution of Scripts/test (3).sql
prompt Starting execution of Scripts/test (5).sql
@@"create/Scripts/test (5).sql"
prompt Finished execution of Scripts/test (5).sql
spool off
quit
set termout on
spool apply.log
prompt Starting execution of script (1).sql
@@"create/script (1).sql"
prompt Finished execution of script (1).sql
prompt Starting execution of script (2).sql
@@"create/script (2).sql"
prompt Finished execution of script (2).sql
prompt Starting execution of script (3).sql
@@"create/script (3).sql"
prompt Finished execution of script (3).sql
spool off
quit
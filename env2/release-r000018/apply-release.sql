set termout on
spool apply.log
prompt Starting execution of dummy.sql
@@"create/dummy.sql"
prompt Finished execution of dummy.sql
spool off
quit
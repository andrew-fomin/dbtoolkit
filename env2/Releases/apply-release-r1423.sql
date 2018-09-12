set termout on
spool apply.log
prompt Starting execution of Create/1.sql
@@"Create/1.sql"
prompt Finished execution of Create/1.sql
spool off
quit
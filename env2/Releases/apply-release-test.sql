set termout on
spool apply.log
prompt Starting execution of PLSQL/1.sql
@@"create/PLSQL/1.sql"
prompt Finished execution of PLSQL/1.sql
spool off
quit
set termout on
spool revert.log
prompt Starting execution of PLSQL/4.sql
@@"PLSQL/4.sql"
prompt Finished execution of PLSQL/4.sql
prompt Starting execution of Table/6.sql
@@"Table/6.sql"
prompt Finished execution of Table/6.sql
spool revert.sql.log
quit
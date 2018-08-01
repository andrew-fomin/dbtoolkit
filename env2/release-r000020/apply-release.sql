set termout on
spool apply.log
prompt Starting execution of dummy.sql
@@"create/dummy.sql"
prompt Finished execution of dummy.sql
prompt Starting execution of Packages/dummy2.sql
@@"create/Packages/dummy2.sql"
prompt Finished execution of Packages/dummy2.sql
spool off
quit
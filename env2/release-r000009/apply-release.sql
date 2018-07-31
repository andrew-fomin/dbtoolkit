set termout off
spool apply.log
prompt Starting execution of Tables/table.sql
@@create/Tables/table.sql
prompt Finished execution of Tables/table.sql
prompt Starting execution of topl.sql
@@create/topl.sql
prompt Finished execution of topl.sql
spool off
quit
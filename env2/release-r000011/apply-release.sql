set termout off
spool apply.log
prompt Starting execution of Tables/table (1).sql
@@create/Tables/table (1).sql
prompt Finished execution of Tables/table (1).sql
prompt Starting execution of Tables/table (2).sql
@@create/Tables/table (2).sql
prompt Finished execution of Tables/table (2).sql
prompt Starting execution of topl.sql
@@create/topl.sql
prompt Finished execution of topl.sql
spool off
quit
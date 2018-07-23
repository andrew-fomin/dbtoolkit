set termout off
spool apply.log
prompt Starting execution of script(1).sql
@@create/script(1).sql
prompt Finished execution of script(1).sql
prompt Starting execution of script(2).sql
@@create/script(2).sql
prompt Finished execution of script(2).sql
prompt Starting execution of script(3).sql
@@create/script(3).sql
prompt Finished execution of script(3).sql
prompt Starting execution of script(4).sql
@@create/script(4).sql
prompt Finished execution of script(4).sql
prompt Starting execution of script(5).sql
@@create/script(5).sql
prompt Finished execution of script(5).sql
prompt Starting execution of script(6).sql
@@create/script(6).sql
prompt Finished execution of script(6).sql
prompt Starting execution of script(7).sql
@@create/script(7).sql
prompt Finished execution of script(7).sql
spool off
quit
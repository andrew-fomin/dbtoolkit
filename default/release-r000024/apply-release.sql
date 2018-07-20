set termout off
spool apply.log
prompt Starting execution of test(6).sql
@@create/test(6).sql
prompt Finished execution of test(6).sql
prompt Starting execution of test(7).sql
@@create/test(7).sql
prompt Finished execution of test(7).sql
prompt Starting execution of test(5).sql
@@create/test(5).sql
prompt Finished execution of test(5).sql
prompt Starting execution of test(2).sql
@@create/test(2).sql
prompt Finished execution of test(2).sql
prompt Starting execution of test(3).sql
@@create/test(3).sql
prompt Finished execution of test(3).sql
prompt Starting execution of test(4).sql
@@create/test(4).sql
prompt Finished execution of test(4).sql
prompt Starting execution of test(8).sql
@@create/test(8).sql
prompt Finished execution of test(8).sql
prompt Starting execution of test(1).sql
@@create/test(1).sql
prompt Finished execution of test(1).sql
spool off
quit
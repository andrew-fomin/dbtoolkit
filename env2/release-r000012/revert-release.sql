set termout off
spool revert.log
prompt Starting execution of rev/script1.sql
@@revert/rev/script1.sql
prompt Finished execution of rev/script1.sql
prompt Starting execution of rev (2)/script1.sql
@@revert/rev (2)/script1.sql
prompt Finished execution of rev (2)/script1.sql
prompt Starting execution of rev (4)/script1.sql
@@revert/rev (4)/script1.sql
prompt Finished execution of rev (4)/script1.sql
prompt Starting execution of rev.sql
@@revert/rev.sql
prompt Finished execution of rev.sql
prompt Starting execution of rev (3)/script1.sql
@@revert/rev (3)/script1.sql
prompt Finished execution of rev (3)/script1.sql
spool revert.sql.log
quit
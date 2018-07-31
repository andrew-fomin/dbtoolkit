set termout off
spool apply.log
prompt Starting execution of D:\RM\dbtoolkit\env2\current-release\create\Tables\table.sql
@@create/D:\RM\dbtoolkit\env2\current-release\create\Tables\table.sql
prompt Finished execution of D:\RM\dbtoolkit\env2\current-release\create\Tables\table.sql
prompt Starting execution of D:\RM\dbtoolkit\env2\current-release\create\topl.sql
@@create/D:\RM\dbtoolkit\env2\current-release\create\topl.sql
prompt Finished execution of D:\RM\dbtoolkit\env2\current-release\create\topl.sql
spool off
quit
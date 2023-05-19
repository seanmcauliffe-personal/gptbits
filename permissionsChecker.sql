SELECT 
    DB_NAME(db_id()) AS [Database Name],
    USER_NAME(p.grantee_principal_id) AS [User Name],
    dp.principal_id,
    dp.type_desc AS [User Type],
    p.class_desc,
    OBJECT_NAME(p.major_id) AS [Object Name],
    p.permission_name,
    p.state_desc AS [Permission State]
FROM 
    sys.database_permissions p
INNER JOIN
    sys.database_principals dp
ON 
    p.grantee_principal_id = dp.principal_id
WHERE 
    dp.name = USER_NAME();  -- Change this to a username if you are checking for a specific user

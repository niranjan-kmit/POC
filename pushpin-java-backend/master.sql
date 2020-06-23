--CREATE USER realtime_user WITH password 'xxx';
CREATE USER realtime_user;
CREATE ROLE realtime_owner; 
DO $$DECLARE _master varchar;
BEGIN
    _master := (SELECT CURRENT_USER::varchar);
    EXECUTE 'GRANT realtime_owner TO '||_master;
END$$;
CREATE DATABASE realtime WITH OWNER = realtime_owner;
GRANT CONNECT ON DATABASE realtime to realtime_owner;
GRANT realtime_owner TO realtime_user;
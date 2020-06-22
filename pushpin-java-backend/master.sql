CREATE USER realtime_user WITH password 'xxx';
CREATE ROLE realtime_owner;
CREATE USER realtime_user 
DO $$DECLARE _master varchar;
BEGIN
    _master := (SELECT CURRENT_USER::varchar);
    EXECUTE 'GRANT realtime_owner TO '||_master;
END$$;
CREATE DATABASE pushpin WITH OWNER = realtime_owner;
GRANT CONNECT ON DATABASE pushpin to realtime_owner;
GRANT realtime_owner TO realtime_user;
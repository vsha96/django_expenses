SELECT * FROM expenses_ticket LIMIT 5;
-- id | ticket_text | pub_date | money | account_id 

SELECT * FROM expenses_bankaccount LIMIT 5;
-- id | account_text | creation_date | money  



CREATE INDEX idx_ticket_text_money ON expenses_ticket (ticket_text, money);

DROP INDEX idx_ticket_text_money;


CREATE INDEX idx_ticket_text_only ON expenses_ticket (ticket_text);
CREATE INDEX idx_ticket_text_only ON expenses_ticket USING gin (to_tsvector('english', ticket_text));
CREATE INDEX idx_ticket_money_only ON expenses_ticket (money);

DROP INDEX idx_ticket_text_only;
DROP INDEX idx_ticket_money_only;

vacuum;


EXPLAIN ANALYZE

SELECT 
    eb.id, 
    eb.account_text, 
    et.ticket_text,
    SUM(et.money) AS total_money_spent,
    -- AVG(et.money) AS average_money_spent,
    COUNT(et.money) AS total_actions
FROM expenses_bankaccount eb
JOIN expenses_ticket      et ON (et.account_id = eb.id)
-- WHERE et.ticket_text = 'pizza'
WHERE LOWER(et.ticket_text) LIKE 'pizza%'
-- WHERE 
--   (to_tsvector('english', ticket_text)) = (to_tsvector('english', 'pizza'))
  AND et.money = 10
GROUP BY eb.id, et.ticket_text
ORDER BY total_money_spent DESC;

-- without index
-- Time: 174.656 ms

-- with index
-- Time: 54.545 ms




SELECT now() wal_capture_time,
        wal_records,
        wal_fpi,
        wal_bytes,
        wal_buffers_full,
        wal_write,
        wal_write_time,
        wal_sync_time,
        stats_reset
FROM   pg_stat_wal;






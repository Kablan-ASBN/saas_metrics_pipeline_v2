-- Run automatically by the Postgres container on first start.
-- Creates the schemas dbt and the seed script that I will use later.
--
-- The schema convention:
--   raw_app     -> landed source data
--   analytics   -> dbt outputs
--   snapshots   -> dbt snapshots

CREATE SCHEMA IF NOT EXISTS raw_app;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS snapshots;
-- Migration: Update prompts table for async processing
ALTER TABLE prompts
    DROP COLUMN IF EXISTS duration_ms,
    ADD COLUMN IF NOT EXISTS started BIGINT NOT NULL DEFAULT (extract(epoch from now())),
    ADD COLUMN IF NOT EXISTS completed BIGINT;

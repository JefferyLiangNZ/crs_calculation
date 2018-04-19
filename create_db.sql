
-- Table: waca.wac_test_rule

-- DROP TABLE waca.wac_test_rule;

CREATE TABLE waca.wac_test_rule
(
  id integer NOT NULL,
  reg_ver character varying(12),
  rule_title character varying(80),
  reg_desc character varying(120),
  rule_desc text,
  rule_block text,
  CONSTRAINT _wac_test_rule_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE waca.wac_test_rule
  OWNER TO gdb_user;

GRANT ALL ON TABLE waca.wac_test_rule TO gdb_user;
GRANT ALL ON TABLE waca.wac_test_rule TO "JLiang";
COMMENT ON COLUMN waca.wac_test_rule.id IS 'auto incremental seq number';
COMMENT ON COLUMN waca.wac_test_rule.reg_ver IS 'version info of test rule, i.e, 2002/2-A, 1998-II';
COMMENT ON COLUMN waca.wac_test_rule.rule_title IS 'combined version of rule title, i.e Reg 28 and 26.2.b.iii';

-- Table: waca.wac_wrk_check_list

-- DROP TABLE waca.wac_wrk_check_list;

CREATE TABLE waca.wac_wrk_check_list
(
  id integer NOT NULL,
  wrk_id integer NOT NULL, -- CSD work id
  chi_code character varying(8), -- CSD check type i.e. C182, C184, C185
  exec_stage character varying(8), -- Stage of CSD Test
  result character varying(8), -- Result of CSD Test(PASS, FAIL, UNTD)
  obn_cnt integer,
  param_cnt integer,
  dof integer,
  stderr_uw numeric(16,8),
  reference_id integer,
  summary_txt text,
  CONSTRAINT _wrk_checks_pkey_t PRIMARY KEY (id),
  CONSTRAINT wac_wrk_check_list_reference_id_key_t UNIQUE (reference_id)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE waca.wac_wrk_check_list
  OWNER TO gdb_user;
GRANT ALL ON TABLE waca.wac_wrk_check_list TO gdb_user;
GRANT ALL ON TABLE waca.wac_wrk_check_list TO "JLiang";
COMMENT ON TABLE waca.wac_wrk_check_list
  IS 'Primary Table for Test plan evaluation';
COMMENT ON COLUMN waca.wac_wrk_check_list.wrk_id IS 'CSD work id';
COMMENT ON COLUMN waca.wac_wrk_check_list.chi_code IS 'CSD check type i.e. C182, C184, C185';
COMMENT ON COLUMN waca.wac_wrk_check_list.exec_stage IS 'Stage of CSD Test';
COMMENT ON COLUMN waca.wac_wrk_check_list.result IS 'Result of CSD Test(PASS, FAIL, UNTD)';

-- Table: waca.wac_test_rule_stats

-- DROP TABLE waca.wac_test_rule_stats;

CREATE TABLE waca.wac_test_rule_stats
(
  id integer NOT NULL,
  chk_id integer NOT NULL,
  rule_id integer NOT NULL,
  fail_cnt integer NOT NULL,
  obn_cnt integer NOT NULL,
  ratio numeric(7,4),
  error numeric(10,5),
  CONSTRAINT wac_test_rule_stats_chk_id_fkey FOREIGN KEY (chk_id)
      REFERENCES waca.wac_wrk_check_list (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT wac_test_rule_stats_rule_id_fkey FOREIGN KEY (rule_id)
      REFERENCES waca.wac_test_rule (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE waca.wac_test_rule_stats
  OWNER TO gdb_user;
GRANT ALL ON TABLE waca.wac_test_rule_stats TO "JLiang";
GRANT ALL ON TABLE waca.wac_test_rule_stats TO gdb_user;

-- Table: waca.wac_wrk_check_ext

-- DROP TABLE waca.wac_wrk_check_ext;

CREATE TABLE waca.wac_wrk_check_ext
(
  wcl_id integer NOT NULL, -- queried from block_data.id by referring ST_WITHIN(shape, block_data.shape)
  wrk_id integer NOT NULL, -- same as wac_wrk_check_list.wrk_id
  reference_id integer,
  shape geometry(Point,4167),
  block_id integer,
  CONSTRAINT wac_wrk_check_ext_wcl_id_fkey FOREIGN KEY (wcl_id)
      REFERENCES waca.wac_wrk_check_list (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT wac_wrk_check_ext_wrk_id_fkey FOREIGN KEY (wrk_id)
      REFERENCES waca.wac_wrk_check_list (wrk_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=TRUE
);

ALTER TABLE waca.wac_wrk_check_ext
  OWNER TO gdb_user;
GRANT ALL ON TABLE waca.wac_wrk_check_ext TO "JLiang";
GRANT ALL ON TABLE waca.wac_wrk_check_ext TO gdb_user;

COMMENT ON TABLE waca.wac_wrk_check_ext 	    IS 'Extened Table for Test plan evaluation';
COMMENT ON COLUMN waca.wac_wrk_check_ext.wcl_id IS 'queried from block_data.id by referring ST_WITHIN(shape, block_data.shape)';
COMMENT ON COLUMN waca.wac_wrk_check_ext.wrk_id IS 'same as wac_wrk_check_list.wrk_id';

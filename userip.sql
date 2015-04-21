--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: locks; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE locks (
    name character(10) NOT NULL,
    acquire boolean DEFAULT false NOT NULL,
    ts timestamp without time zone NOT NULL
);


--
-- Name: user_ip; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE user_ip (
    id integer NOT NULL,
    user_id integer NOT NULL,
    ip inet NOT NULL,
    ts timestamp without time zone NOT NULL
);


--
-- Name: user_ip_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE user_ip_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_ip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE user_ip_id_seq OWNED BY user_ip.id;


--
-- Name: users_link; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE users_link (
    u1_id integer NOT NULL,
    u2_id integer NOT NULL,
    ips inet[] NOT NULL,
    match boolean DEFAULT false NOT NULL
);


--
-- Name: vars; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE vars (
    last_user_ip_id integer
);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_ip ALTER COLUMN id SET DEFAULT nextval('user_ip_id_seq'::regclass);


--
-- Data for Name: locks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY locks (name, acquire, ts) FROM stdin;
link_proc 	f	2015-04-21 08:47:41.994008
\.


--
-- Data for Name: user_ip; Type: TABLE DATA; Schema: public; Owner: -
--

COPY user_ip (id, user_id, ip, ts) FROM stdin;
\.


--
-- Name: user_ip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('user_ip_id_seq', 1, false);


--
-- Data for Name: users_link; Type: TABLE DATA; Schema: public; Owner: -
--

COPY users_link (u1_id, u2_id, ips, match) FROM stdin;
\.


--
-- Data for Name: vars; Type: TABLE DATA; Schema: public; Owner: -
--

COPY vars (last_user_ip_id) FROM stdin;
\N
\.


--
-- Name: locks_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY locks
    ADD CONSTRAINT locks_pkey PRIMARY KEY (name);


--
-- Name: user_ip_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY user_ip
    ADD CONSTRAINT user_ip_pkey PRIMARY KEY (id);


--
-- Name: users_link_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY users_link
    ADD CONSTRAINT users_link_pkey PRIMARY KEY (u1_id, u2_id);


--
-- Name: user_ip_ip_user_id_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX user_ip_ip_user_id_idx ON user_ip USING btree (ip, user_id);


--
-- PostgreSQL database dump complete
--


-- Adminer 4.8.1 PostgreSQL 16.4 dump

DROP TABLE IF EXISTS "orderitem";
DROP SEQUENCE IF EXISTS orderitem_id_seq;
CREATE SEQUENCE orderitem_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orderitem" (
    "id" integer DEFAULT nextval('orderitem_id_seq') NOT NULL,
    "order_id" integer,
    "product_id" integer,
    "amount" integer,
    CONSTRAINT "orderitem_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "ix_orderitem_id" ON "public"."orderitem" USING btree ("id");

CREATE INDEX "ix_orderitem_order_id" ON "public"."orderitem" USING btree ("order_id");

CREATE INDEX "ix_orderitem_product_id" ON "public"."orderitem" USING btree ("product_id");

INSERT INTO "orderitem" ("id", "order_id", "product_id", "amount") VALUES
(1,	1,	1,	13),
(2,	2,	1,	2),
(3,	2,	2,	1),
(4,	3,	3,	1),
(5,	4,	3,	5),
(6,	4,	2,	11),
(7,	5,	3,	1);

DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS order_id_seq;
CREATE SEQUENCE order_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "id" integer DEFAULT nextval('order_id_seq') NOT NULL,
    "create_data" timestamp,
    "status" character varying,
    CONSTRAINT "order_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "ix_order_id" ON "public"."orders" USING btree ("id");

INSERT INTO "orders" ("id", "create_data", "status") VALUES
(1,	'2024-09-26 15:40:11.680257',	'Отправлен'),
(2,	'2024-09-26 15:42:32.443891',	'Отправлен'),
(3,	'2024-09-27 12:15:20.151178',	'Отправлен'),
(5,	'2024-09-27 14:20:08.502031',	'В процессе'),
(4,	'2024-09-27 14:19:07.485099',	'Отправлен');

DROP TABLE IF EXISTS "product";
DROP SEQUENCE IF EXISTS product_id_seq;
CREATE SEQUENCE product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."product" (
    "id" integer DEFAULT nextval('product_id_seq') NOT NULL,
    "name" character varying,
    "descr" character varying,
    "price" double precision,
    "total_amount" integer,
    CONSTRAINT "product_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "ix_product_id" ON "public"."product" USING btree ("id");

CREATE INDEX "ix_product_name" ON "public"."product" USING btree ("name");

INSERT INTO "product" ("id", "name", "descr", "price", "total_amount") VALUES
(1,	'phone',	'good',	17890,	485),
(2,	'mouse',	'verygood',	2500,	88),
(3,	'table',	'wooden',	1000,	3);

ALTER TABLE ONLY "public"."orderitem" ADD CONSTRAINT "orderitem_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orderitem" ADD CONSTRAINT "orderitem_product_id_fkey" FOREIGN KEY (product_id) REFERENCES product(id) NOT DEFERRABLE;

-- 2024-09-29 11:05:23.114307+00

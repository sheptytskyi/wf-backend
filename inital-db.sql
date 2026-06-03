CREATE TYPE "user_role" AS ENUM (
  'SUPERADMIN',
  'OWNER',
  'REALTOR',
  'MARKETER',
  'VIEWER'
);

CREATE TYPE "deal_type" AS ENUM (
  'SALE',
  'RENT'
);

CREATE TYPE "contact_preference" AS ENUM (
  'EMAIL',
  'PHONE',
  'WHATSAPP',
  'TELEGRAM'
);

CREATE TYPE "booking_status" AS ENUM (
  'PENDING',
  'CONFIRMED',
  'CANCELED',
  'RESCHEDULED',
  'COMPLETED',
  'NO_SHOW'
);

CREATE TYPE "subscription_status" AS ENUM (
  'TRIAL',
  'ACTIVE',
  'PAST_DUE',
  'CANCELED'
);

CREATE TABLE "subscription_plans" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "name" varchar NOT NULL,
  "max_realtors" int NOT NULL,
  "max_properties" int NOT NULL,
  "price_monthly" decimal(10,2) NOT NULL,
  "features" jsonb
);

CREATE TABLE "companies" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "plan_id" uuid,
  "name" varchar NOT NULL,
  "slug" varchar UNIQUE NOT NULL,
  "subscription_status" subscription_status DEFAULT 'TRIAL',
  "analytics_meta" jsonb,
  "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "company_id" uuid,
  "role" user_role NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "password_hash" varchar NOT NULL,
  "first_name" varchar,
  "last_name" varchar,
  "calendar_sync_data" jsonb,
  "is_active" boolean DEFAULT true,
  "last_login_at" timestamptz,
  "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "countries" (
  "id" int PRIMARY KEY,
  "title" varchar
);

CREATE TABLE "cities" (
  "id" int PRIMARY KEY,
  "title" varchar
);

CREATE TABLE "properties" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "company_id" uuid,
  "title" varchar NOT NULL,
  "address_str" text NOT NULL,
  "country" int,
  "city" int,
  "deal_type" deal_type NOT NULL,
  "price" decimal(12,2) NOT NULL,
  "currency" varchar(3) DEFAULT 'USD',
  "area_total" float NOT NULL,
  "rooms_count" int NOT NULL,
  "valid_from" timestamptz NOT NULL,
  "valid_until" timestamptz NOT NULL,
  "is_active" boolean DEFAULT true,
  "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "property_realtors" (
  "property_id" uuid,
  "user_id" uuid,
  "primary_realtor" boolean DEFAULT false,
  PRIMARY KEY ("property_id", "user_id")
);

CREATE TABLE "property_images" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "property_id" uuid,
  "s3_key" varchar NOT NULL,
  "is_main" boolean DEFAULT false,
  "order_index" int DEFAULT 0
);

CREATE TABLE "clients" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "email" varchar UNIQUE,
  "phone" varchar,
  "first_name" varchar,
  "last_name" varchar,
  "pref_contact" contact_preference DEFAULT 'EMAIL',
  "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "availability_slots" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "property_id" uuid,
  "realtor_id" uuid,
  "start_time" timestamptz NOT NULL,
  "end_time" timestamptz NOT NULL,
  "is_booked" boolean DEFAULT false
);

CREATE TABLE "bookings" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "slot_id" uuid UNIQUE,
  "client_id" uuid,
  "status" booking_status DEFAULT 'PENDING',
  "cancel_reason" text,
  "utm_source" varchar,
  "utm_medium" varchar,
  "utm_campaign" varchar,
  "device_type" varchar,
  "browser_lang" varchar,
  "ip_country" varchar,
  "seconds_to_book" int,
  "created_at" timestamptz DEFAULT (now()),
  "updated_at" timestamptz
);

CREATE TABLE "reviews" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "booking_id" uuid UNIQUE,
  "realtor_id" uuid,
  "rating" int NOT NULL,
  "feedback_text" text,
  "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "booking_history" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "booking_id" uuid,
  "action" varchar NOT NULL,
  "old_data" jsonb,
  "new_data" jsonb,
  "changed_at" timestamptz DEFAULT (now())
);

CREATE INDEX ON "users" ("email");

CREATE INDEX ON "users" ("company_id");

CREATE INDEX ON "properties" ("company_id");

CREATE INDEX ON "properties" ("valid_from", "valid_until");

CREATE INDEX ON "properties" ("price");

CREATE INDEX ON "availability_slots" ("property_id", "realtor_id", "start_time");

CREATE INDEX ON "availability_slots" ("is_booked");

CREATE INDEX ON "bookings" ("client_id");

CREATE INDEX ON "bookings" ("status");

CREATE INDEX ON "bookings" ("created_at");

CREATE INDEX ON "reviews" ("realtor_id");

CREATE INDEX ON "reviews" ("rating");

COMMENT ON COLUMN "companies"."analytics_meta" IS 'Звідки прийшла компанія';

COMMENT ON COLUMN "users"."company_id" IS 'null for superadmins';

COMMENT ON COLUMN "users"."calendar_sync_data" IS 'Tokens for Google/Outlook';

COMMENT ON COLUMN "property_images"."s3_key" IS 'Path in S3 bucket';

COMMENT ON COLUMN "clients"."id" IS 'Stored in cookie';

COMMENT ON COLUMN "bookings"."cancel_reason" IS 'Optional';

COMMENT ON COLUMN "bookings"."seconds_to_book" IS 'Time spent on page before booking';

COMMENT ON COLUMN "reviews"."rating" IS '1 to 5';

ALTER TABLE "companies" ADD FOREIGN KEY ("plan_id") REFERENCES "subscription_plans" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "users" ADD FOREIGN KEY ("company_id") REFERENCES "companies" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "properties" ADD FOREIGN KEY ("company_id") REFERENCES "companies" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "properties" ADD FOREIGN KEY ("country") REFERENCES "countries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "properties" ADD FOREIGN KEY ("city") REFERENCES "cities" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "property_realtors" ADD FOREIGN KEY ("property_id") REFERENCES "properties" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "property_realtors" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "property_images" ADD FOREIGN KEY ("property_id") REFERENCES "properties" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "availability_slots" ADD FOREIGN KEY ("property_id") REFERENCES "properties" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "availability_slots" ADD FOREIGN KEY ("realtor_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "bookings" ADD FOREIGN KEY ("slot_id") REFERENCES "availability_slots" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "bookings" ADD FOREIGN KEY ("client_id") REFERENCES "clients" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("booking_id") REFERENCES "bookings" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("realtor_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "booking_history" ADD FOREIGN KEY ("booking_id") REFERENCES "bookings" ("id") DEFERRABLE INITIALLY IMMEDIATE;

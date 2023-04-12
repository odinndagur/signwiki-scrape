CREATE TABLE IF NOT EXISTS "sign_collection" (
        "sign_id"       INTEGER,
        "collection_id" INTEGER,
        "date_added"    DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("sign_id","collection_id"),
        FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
        FOREIGN KEY("collection_id") REFERENCES "collection"("id")
);
CREATE TABLE IF NOT EXISTS "user" (
        "id"    INTEGER,
        "name"  TEXT NOT NULL UNIQUE,
        "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "sign_related" (
        "sign_id"       INTEGER,
        "related_id"    INTEGER,
        PRIMARY KEY("sign_id","related_id"),
        FOREIGN KEY("related_id") REFERENCES "sign"("id"),
        FOREIGN KEY("sign_id") REFERENCES "sign"("id")
);
CREATE TABLE IF NOT EXISTS "collection" (
        "id"    INTEGER,
        "user_id"       INTEGER,
        "name"  INTEGER,
        "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id"),
        FOREIGN KEY("user_id") REFERENCES "user"("id")
);

CREATE TABLE IF NOT EXISTS "sign" (
        "id"    INTEGER,
        "phrase"        TEXT NOT NULL UNIQUE,
        PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "efnisflokkur"(
    "id" INTEGER PRIMARY KEY,
    "text" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "sign_efnisflokkur"(
    "sign_id" INTEGER,
    "efnisflokkur_id" INTEGER,
    "rank" INTEGER,
    PRIMARY KEY("sign_id","efnisflokkur_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("efnisflokkur_id") REFERENCES "efnisflokkur"("id")
);

CREATE TABLE IF NOT EXISTS "islenska"(
    "sign_id" INTEGER,
    "text" TEXT NOT NULL,
    PRIMARY KEY("sign_id","text"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id")
);

CREATE TABLE IF NOT EXISTS "sign_munnhreyfing"(
    "sign_id" INTEGER,
    "munnhreyfing_id" INTEGER,
    "rank" INTEGER,
    PRIMARY KEY("sign_id","munnhreyfing_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("munnhreyfing_id") REFERENCES "munnhreyfing"("id")
);

CREATE TABLE IF NOT EXISTS "munnhreyfing"(
    "id" INTEGER PRIMARY KEY,
    "text" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "myndatexti"(
    "sign_id" INTEGER,
    "text" TEXT NOT NULL,
    FOREIGN KEY("sign_id") REFERENCES "sign"("id")
);

CREATE TABLE IF NOT EXISTS "sign_myndunarstadur"(
    "sign_id" INTEGER,
    "rank" INTEGER,
    "myndunarstadur_id" INTEGER,
    PRIMARY KEY("sign_id","myndunarstadur_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("myndunarstadur_id") REFERENCES "myndunarstadur"("id")
);

CREATE TABLE IF NOT EXISTS "myndunarstadur"(
    "id" INTEGER PRIMARY KEY,
    "text" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "sign_ordflokkur"(
    "sign_id" INTEGER,
    "ordflokkur_id" INTEGER,
    "rank" INTEGER,
    PRIMARY KEY("sign_id","ordflokkur_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("ordflokkur_id") REFERENCES "ordflokkur"("id")
);

CREATE TABLE IF NOT EXISTS "ordflokkur"(
    "id" INTEGER PRIMARY KEY,
    "text" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "sign_handform"(
    "sign_id" INTEGER,
    "handform_id" INTEGER,
    "rank" INTEGER,
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("handform_id") REFERENCES "handform"("id")
);

CREATE TABLE IF NOT EXISTS "handform"(
    "handform_id" INTEGER PRIMARY KEY,
    "text"
);

CREATE TABLE IF NOT EXISTS "sign_twohandforms"(
    "sign_id" INTEGER,
    "twohandforms_id" INTEGER,
    "rank" INTEGER,
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("twohandforms_id") REFERENCES "twohandforms"("id")
);

CREATE TABLE IF NOT EXISTS "twohandforms"(
    "id" INTEGER PRIMARY KEY,
    "text" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "sign_video"(
    "video_id" TEXT PRIMARY KEY,
    "sign_id" INTEGER,
    "rank" INTEGER,
    PRIMARY KEY("sign_id","video_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id")
);

CREATE TABLE IF NOT EXISTS "sign_related"(
    "sign_id" INTEGER,
    "related_id" INTEGER,
    "rank" INTEGER,
    PRIMARY KEY("sign_id","related_id"),
    FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
    FOREIGN KEY("related_id") REFERENCES "sign"("id")
);

CREATE INDEX idx_sign_phrase ON sign(phrase);
CREATE INDEX idx_sign_youtube_id ON sign(youtube_id);
CREATE INDEX idx_sign_id ON sign(id);
CREATE INDEX idx_sign_related_sign_id ON sign_related(sign_id);
CREATE INDEX idx_sign_related_related_id ON sign_related(related_id);
CREATE INDEX idx_sign_collection_sign_id ON sign_collection(sign_id);
CREATE INDEX idx_sign_collection_collection_id ON sign_collection(collection_id);
CREATE INDEX idx_sign_related_sign_id_related_id ON sign_related(sign_id,related_id);
CREATE INDEX idx_sign_collection_sign_collection_id ON sign_collection(sign_id,collection_id);
CREATE INDEX idx_sign_related_related_id_sign_id ON sign_related(related_id,sign_id);
CREATE INDEX idx_collection_name on collection(name);
CREATE INDEX idx_collection_name_id on collection(name,id);
CREATE INDEX idx_collection_id_name on collection(id,name);
CREATE INDEX idx_multi on sign (phrase, id);
CREATE INDEX idx_sign on sign (phrase);
CREATE INDEX idx_sign_all on sign (phrase,id,youtube_id,youtube_link);
CREATE INDEX idx_sign_yt_id on sign (youtube_id);
CREATE INDEX idx_sign_yt_link on sign (youtube_link);
CREATE INDEX idx_sign_phrase_yt_link on sign (phrase,youtube_link);

CREATE VIRTUAL TABLE sign_fts USING FTS5(id,phrase,related_signs)

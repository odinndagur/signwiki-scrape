
CREATE TABLE IF NOT EXISTS sign(
    id INTEGER PRIMARY KEY,
    phrase TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS efnisflokkur(
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL
)
CREATE TABLE IF NOT EXISTS sign_efnisflokkur(
    sign_id INTEGER,
    efnisflokkur_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(efnisflokkur_id) REFERENCES efnisflokkur(id)
)

CREATE TABLE IF NOT EXISTS islenska(
    sign_id INTEGER,
    text TEXT NOT NULL,
    FOREIGN KEY(sign_id) REFERENCES sign(id)
)
CREATE TABLE IF NOT EXISTS sign_munnhreyfing(
    sign_id INTEGER,
    munnhreyfing_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(munnhreyfing_id) REFERENCES munnhreyfing(id)
)
CREATE TABLE IF NOT EXISTS munnhreyfing(
    munnhreyfing_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL
)
CREATE TABLE IF NOT EXISTS myndatexti(
    sign_id INTEGER,
    text TEXT NOT NULL,
    FOREIGN KEY(sign_id) REFERENCES sign(id)

)
CREATE TABLE IF NOT EXISTS sign_myndunarstadur(
    sign_id INTEGER,
    rank INTEGER,
    myndunarstadur_id INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(myndunarstadur_id) REFERENCES myndunarstadur(id)
)
CREATE TABLE IF NOT EXISTS myndunarstadur(
    myndunarstadur_id INTEGER,
    text TEXT NOT NULL
)
CREATE TABLE IF NOT EXISTS sign_ordflokkur(
    sign_id INTEGER,
    ordflokkur_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(ordflokkur_id) REFERENCES ordflokkur(id)
)
CREATE TABLE IF NOT EXISTS ordflokkur(
    ordflokkur_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL
)
CREATE TABLE IF NOT EXISTS sign_handform(
    sign_id INTEGER,
    handform_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(handform_id) REFERENCES handform(id)
)
CREATE TABLE IF NOT EXISTS handform(
    handform_id INTEGER PRIMARY KEY,
    text
)
CREATE TABLE IF NOT EXISTS sign_twohandforms(
    sign_id INTEGER,
    twohandforms_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(twohandforms_id) REFERENCES twohandforms(id)

)
CREATE TABLE IF NOT EXISTS twohandforms(
    twohandforms_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS sign_related(
    sign_id INTEGER,
    related_id INTEGER,
    rank INTEGER,
    FOREIGN KEY(sign_id) REFERENCES sign(id),
    FOREIGN KEY(related_id) REFERENCES sign(id)
);
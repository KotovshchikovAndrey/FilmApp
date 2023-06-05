FIND_USER_BY_EMAIL = """SELECT * FROM "user" WHERE email = :email;"""
FIND_USER_BY_ID = """SELECT * FROM "user" WHERE id = :id;"""
CREATE_NEW_USER = """INSERT INTO "user" (id, name, surname, email, password, avatar, status, role, refresh_tokens, reset_codes)
    VALUES (DEFAULT, :name, :surname, :email, :password, null, 'not_verified'::user_status, 'user'::user_role, DEFAULT,
        DEFAULT);
"""
ADD_NEW_VERIFICATION_CODE = """UPDATE "user"
SET reset_codes = reset_codes || PASTE_JSON_HERE::jsonb
WHERE email = :email;
"""
FIND_USER_WITH_CODE = """SELECT *
FROM "user", jsonb_array_elements(reset_codes) as rc
WHERE email = :email
AND rc->>'code' = :code;
"""
VERIFY_USER = """UPDATE "user"
SET status = 'active'
WHERE id = :id;
"""
CLEAR_CODES = """UPDATE "user"
SET reset_codes = '[]'::jsonb
WHERE id = :id;
"""
ADD_REFRESH_TOKEN = """UPDATE "user"
SET refresh_tokens = array_append(refresh_tokens, :refresh_token)
WHERE id = :id;
"""
DELETE_REFRESH_TOKEN = """UPDATE "user"
SET refresh_tokens = array_remove(refresh_tokens, :refresh_token)
WHERE id = :id;
"""
DELETE_ALL_REFRESH_TOKENS = """UPDATE "user"
SET refresh_tokens = '{}'::text[]
WHERE id = :id;
"""

UPDATE_REFRESH_TOKEN = """UPDATE "user"
SET refresh_tokens = array_replace(refresh_tokens, :old_token, :new_token)
WHERE id = :target_id;
"""

CHECK_REFRESH_TOKEN = """SELECT *
FROM "user"
WHERE id = :target_id AND :refresh_token = ANY(refresh_tokens);
"""

CHECK_PASSWORD = """SELECT *
FROM "user"
WHERE id = :id AND password = :password;"""

CHANGE_USER_PASSWORD = """UPDATE "user"
SET password = :password
WHERE id = :id;"""

AUTHORISE_USER = """SELECT * FROM "user" WHERE email = :email and password = :password;"""

CHANGE_WATCH_STATUS = """INSERT INTO watchstatus_user_film(user_id, film_id, status)
VALUES (:user_id, :film_id, :watch_status)
ON CONFLICT (user_id, film_id)
DO UPDATE SET status = EXCLUDED.status;
"""

ADD_FAVORITE_FILM_FOR_USER = """INSERT INTO "favorite_user_film"
(user_id, film_id)
SELECT :user_id, :film_id WHERE NOT EXISTS 
(SELECT * FROM "favorite_user_film" WHERE user_id = :user_id AND film_id = :film_id);"""

DELETE_FAVORITE_FILM_FROM_USER = """DELETE FROM "favorite_user_film"
WHERE user_id = :user_id AND film_id = :film_id"""

CHANGE_USER_STATUS = """UPDATE "user"
SET status = :status
WHERE id = :id;"""

UPDATE_PROFILE_FIELDS = """UPDATE "user" SET 
name = :name,
surname = :surname
WHERE id = :user_id;"""

SET_AVATAR_FOR_USER = """UPDATE "user" SET
avatar = :avatar
WHERE id = :user_id
RETURNING avatar as avatar_url;"""

TOGGLE_USER_VISIBILITY = """UPDATE "user"
SET is_public = :visible
WHERE id = :user_id;"""

CHANGE_USER_EMAIL = """UPDATE "user" SET
email = :new_email
WHERE id = :user_id"""

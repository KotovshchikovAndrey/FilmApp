FIND_USER_BY_EMAIL = (
    """SELECT * FROM "user" WHERE email = :email;"""
)
FIND_USER_BY_ID = (
    """SELECT * FROM "user" WHERE id = :id;"""
)
CREATE_NEW_USER = (
    """INSERT INTO "user" (id, name, surname, email, password, avatar, status, role, refresh_tokens, reset_codes)
    VALUES (DEFAULT, :name, :surname, :email, :password, null, 'not_verified'::user_status, 'user'::user_role, DEFAULT,
        DEFAULT);
"""
)
ADD_NEW_VERIFICATION_CODE = (
    """UPDATE "user"
SET reset_codes = reset_codes || PASTE_JSON_HERE::jsonb
WHERE email = :email;
"""
)
FIND_USER_WITH_CODE = (
    """SELECT *
FROM "user", jsonb_array_elements(reset_codes) as rc
WHERE email = :email
AND rc->>'code' = :code;
"""
)
VERIFY_USER = (
    """UPDATE "user"
SET status = 'active', reset_codes = '[]'::jsonb
WHERE id = :id;
"""
)
ADD_REFRESH_TOKEN = (
    """UPDATE "user"
SET refresh_tokens = array_append(refresh_tokens, :refresh_token)
WHERE id = :id;

"""
)
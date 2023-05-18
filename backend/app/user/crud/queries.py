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
AUTHORISE_USER = (
    """SELECT * FROM "user" WHERE email = :email and password = :password;"""
)
#TODO: сделать удаление токена
#TODO: сделать удаление всех токенов
UPDATE_REFRESH_TOKEN = (
    """UPDATE "user"
SET refresh_tokens = array_replace(refresh_tokens, :old_token, :new_token)
WHERE id = :target_id;
"""
)
CHECK_REFRESH_TOKEN = (
    """SELECT *
FROM "user"
WHERE id = :target_id AND :refresh_token = ANY(refresh_tokens);
"""
)
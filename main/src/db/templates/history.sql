SELECT
    u.id as user_id,
    p.id_post,
    c.created,
    f.id_franchise,
    c.text,
    IF(c.message_type IN (15),"chatbot","human") as speaker
FROM
    auth_user u
    INNER JOIN comments c
        ON u.id = c.id_user
    INNER JOIN posts p
        ON c.id_post = p.id_post
    INNER JOIN franchises f
        ON p.id_franchise = f.id_franchise
WHERE
    message_type NOT IN (14)
    AND u.id = __user_id
    AND f.id_franchise = __franchise_id
ORDER BY
    c.created asc
LIMIT __limit

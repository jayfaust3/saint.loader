SAINT_CREATE_AND_UPDATE_QUERY: str = '''
    INSERT INTO {saint_lake}
    (
        id,
        created_date,
        modified_date,
        active,
        name,
        year_of_birth,
        year_of_death,
        region,
        martyred,
        notes,
        has_avatar
    )
    VALUES
    (
        {id},
        {created_date},
        {modified_date},
        TRUE
        {name},
        {year_of_birth},
        {year_of_death},
        {region},
        {martyred},
        {notes},
        {has_avatar}
    )
'''

SAINT_DELETE_QUERY: str = '''
    INSERT INTO {saint_lake}
    (
        id,
        created_date,
        modified_date,
        active,
        name,
        year_of_birth,
        year_of_death,
        region,
        martyred,
        notes,
        has_avatar
    )
    SELECT
        id,
        created_date,
        modified_date,
        active,
        name,
        year_of_birth,
        year_of_death,
        region,
        martyred,
        notes,
        has_avatar
    FROM
    (
        SELECT
            id,
            created_date,
            modified_date,
            FALSE as active,
            name,
            year_of_birth,
            year_of_death,
            region,
            martyred,
            notes,
            has_avatar,
            ROW_NUMBER() OVER(PARTITION BY id ORDER BY system_id DESC) as recency
        FROM saint_lake
    ) AS grouped
    WHERE
        grouped.recency = 1
'''

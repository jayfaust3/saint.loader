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
    SELECT TOP 1
        id,
        created_date,
        modified_date,
        FALSE,
        name,
        year_of_birth,
        year_of_death,
        region,
        martyred,
        notes,
        has_avatar
        over (PARTITION BY system_id)
    FROM {saint_lake}
    ORDER BY system_id DESC
'''

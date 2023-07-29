class Saint(object):
    def __init__(self,
                 saint_id: str,
                 created_date: int,
                 modified_date: int,
                 name: str,
                 year_of_birth: int,
                 year_of_death: int,
                 region: str,
                 martyred: bool,
                 notes: str,
                 has_avatar: bool) -> None:
        self.id: str = saint_id,
        self.created_date: int = created_date
        self.modified_date: int = modified_date
        self.name: str = name
        self.year_of_birth: int = year_of_birth
        self.year_of_death: int = year_of_death
        self.region: str = region
        self.martyred: bool = martyred
        self.notes: str = notes
        self.has_avatar: bool = has_avatar

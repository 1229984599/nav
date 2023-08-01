from models import Site


class SiteSchemaList(Site.schema_list()):
    pass


class SiteSchemaUpdate(Site.schema_update()):
    id: int | str | None
    pass

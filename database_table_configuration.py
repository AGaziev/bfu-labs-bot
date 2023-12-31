def configure_and_fill_database_tables() -> None:
    from repositories import db
    import utils.models
    db.create_tables([utils.models.User,
                      utils.models.Teacher,
                      utils.models.Group,
                      utils.models.GroupMember,
                      utils.models.LabRegistry,
                      utils.models.Status,
                      utils.models.LabWork])


if __name__ == '__main__':
    configure_and_fill_database_tables()

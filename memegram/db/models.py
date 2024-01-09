from contextlib import contextmanager

from peewee import Model, DeferredThroughModel, SqliteDatabase, CharField, ForeignKeyField, ManyToManyField

from memegram.db import DB_FILE_PATH

db = SqliteDatabase(DB_FILE_PATH)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @contextmanager
    def transaction(cls):
        with cls._meta.database.atomic():
            yield

ImageTagThroughDeferred = DeferredThroughModel()

class Image(BaseModel):
    class Meta:
        table_name = "images"

    filename = CharField()
    filepath = CharField()
    digest = CharField(unique=True)

    def __repr__(self):
        return (
            f"<Image(id: {self.id}, filename: {self.filename}, "
            f"filepath: {self.filepath}, digest: {self.digest}>"
        )

class Tag(BaseModel):
    class Meta:
        table_name = "tags"

    name = CharField(unique=True)
    images = ManyToManyField(Image, through_model=ImageTagThroughDeferred, backref="tags")

class ImageTag(BaseModel):
    class Meta:
        table_name = 'image_tags'

    tags = ForeignKeyField(Tag, backref="image_tags")
    images = ForeignKeyField(Image, backref="image_tags")

ImageTagThroughDeferred.set_model(ImageTag)

Image.create_table()
Tag.create_table()
ImageTag.create_table()

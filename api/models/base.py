from pydantic import ConfigDict
from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    create_time = fields.DatetimeField(null=True, auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(null=True, auto_now=True, description="更新时间")


class AppModel(Model, TimestampMixin):
    id = fields.IntField(pk=True, index=True, description="主键")
    status = fields.BooleanField(null=False, default=True, index=True, description="状态")

    class PydanticMeta:
        backward_relations = False
        model_config = ConfigDict(extra="ignore", strict=False)

    class Meta:
        abstract = True
        ordering = ["-update_time", "-create_time"]


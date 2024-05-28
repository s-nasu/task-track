from datetime import datetime
from typing import Any, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class FormattedDatetime(datetime):
    """
    入力されたdatetimeをそのまま返す特殊なdatetime型です。
    （シリアライズ専用）
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        このクラスのPydanticコアスキーマを返します。このスキーマは、
        このクラスが入力としてdatetimeを受け取り、それを'%Y-%m-%d %H:%M:%S'の
        形式の文字列としてシリアライズすることを示しています。
        """
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.format_ser_schema("%Y-%m-%d %H:%M:%S"),
        )

    @classmethod
    def _validate(cls, v: datetime):
        """
        入力値を検証します。このメソッドは入力されたdatetimeをそのまま返します。
        """
        return v

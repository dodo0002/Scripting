from pydantic import BaseModel, Field, conint, ConfigDict
from typing import Annotated
from datetime import datetime

# 用於新增 (POST) 和更新 (PUT) 的資料驗證

priceDaUZero = Annotated[int, Field(gt=0)]


class BookCreate(BaseModel):
    """
    用於新增和更新書籍資料的輸入驗證
    所有欄位都是非必須的，但Price必須大於 0
    """

    title: str | None = None
    author: str | None = None
    publisher: str | None = None

    # 確保 price 必須大於 0
    price: priceDaUZero | None = Field(None)

    publish_date: str | None = Field(None, example="YYYY-MM-DD")
    isbn: str | None = None
    cover_url: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "LLM 應用開發實戰",
                "author": "AI 大師",
                "price": 580,
            }
        }
    )


# 用於 API 回傳的資料

class BookResponse(BaseModel):
    """
    用於 API 回傳給客戶端的書籍資料
    確保包含 id 和 created_at 欄位
    """
    id: int = Field(..., description="書籍的唯一識別 ID")
    title: str
    author: str
    publisher: str | None = None
    price: int
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None

    # created_at 必須是 datetime 物件，用於回傳
    created_at: datetime = Field(..., description="記錄建立的時間戳")

    model_config = ConfigDict(from_attributes=True)

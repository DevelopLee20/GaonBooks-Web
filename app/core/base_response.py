from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    detail: str = Field(..., description="응답 결과", examples=["응답 결과"])
    status_code: int
    # data: BaseModel

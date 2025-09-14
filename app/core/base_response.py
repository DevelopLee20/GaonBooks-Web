from pydantic import BaseModel, Field, ConfigDict  # Import ConfigDict


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Add this line
    detail: str = Field(..., description="응답 결과", examples=["응답 결과"])
    status_code: int
    # data: BaseModel

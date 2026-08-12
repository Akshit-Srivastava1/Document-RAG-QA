from pydantic import BaseModel, Field

class UploadResponse(BaseModel):
    status: str = Field(..., example="success")
    filename: str = Field(..., example="Operating_System.pdf")
    chunks: int = Field(..., example=42)
    message: str = Field(..., example="PDF uploaded and indexed successfully.")

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        example="What is Deadlock?"
    )

class QuestionResponse(BaseModel):
    answer: str
    source_pages: list[int]

class ErrorResponse(BaseModel):
    status: str
    detail: str
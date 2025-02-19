from pydantic import EmailStr, Field, BaseModel
"""
ImportError: email-validator is not installed, run `pip install pydantic[email]`
"""
class UserBaseSchema(BaseModel):
    """User base schema."""
    email: EmailStr | None = Field(default=None)

user = UserBaseSchema()
user.email = 'vasyaailru'
print(user)
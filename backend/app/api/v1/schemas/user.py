from pydantic import BaseModel, EmailStr


class UserFullInfo(BaseModel):
    id: int 
    name: str 
    bio: str 
    username: str 
    email: str 
    active: bool 
    verified: bool 
    role: str # this is just "user" for now

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            bio=user.bio,
            username=user.username,
            email=user.email,
            active=user.active,
            verified=user.verified,
            role="user",
        )

class UserPublicInfo(BaseModel):
    id: int 
    name: str 
    bio: str 
    username: str 
    active: bool 
    verified: bool 
    role: str # this is just "user" for now

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            bio=user.bio,
            username=user.username,
            active=user.active,
            verified=user.verified,
            role="user",
        )

class APIKeyResponse(BaseModel):
    api_key: str

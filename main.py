from fastapi import FastAPI, File, UploadFile, HTTPException, Form

from bson import ObjectId
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


from models.models import UserProfile
from config.database import get_database
from schemas.users import create_user_profile, update_user_profile, get_user_profile, upload_profile_picture
import uvicorn

app = FastAPI()


# Configure CORS (Cross-Origin Resource Sharing)
origins = ["*"]  # middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get a reference to the MongoDB database
db = get_database()
collection = db["profiles"]

#creating or updating user profile
@app.post("/create_profile/")
async def create_profile(name: str = Form(...), email: str = Form(...), profile_picture: UploadFile = File(...)):
    profile_picture_path = upload_profile_picture(profile_picture)
    profile_id = create_user_profile(name, email, profile_picture_path)
    return {"message": "Profile created successfully", "profile_id": str(profile_id)}

#updating existing profile
@app.put("/update_profile/{profile_id}")
async def update_profile(
        profile_id: str,
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        profile_picture: Optional[UploadFile] = File(None),
):
    profile = get_user_profile(profile_id)
    if not profile:  #validate user
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile_picture:
        profile_picture_path = upload_profile_picture(profile_picture)
    else:
        profile_picture_path = profile["profile_picture"]

    if update_user_profile(profile_id, name, email, profile_picture_path):
        return {"message": "Profile updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update profile")

#retrieve user profile information
@app.get("/get_profile/{profile_id}")
async def read_profile(profile_id: str):
    profile = get_user_profile(profile_id)
    if profile:
        return profile
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


if __name__=='__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
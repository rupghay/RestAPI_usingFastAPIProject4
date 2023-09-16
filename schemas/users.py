from fastapi import FastAPI, File, UploadFile, HTTPException, Form


# Create a new user profile
def create_user_profile(name, email, profile_picture):
    profile = {
        "name": name,
        "email": email,
        "profile_picture": profile_picture,
    }
    return collection.insert_one(profile).inserted_id


# Update user profile by ID
def update_user_profile(profile_id, name=None, email=None,profile_picture=None):
    update_fields = {}
    if name is not None:
        update_fields["name"] = name
    if email is not None:
        update_fields["email"] = email
    if profile_picture is not None:
        update_fields["profile_picture"] = profile_picture

    updated_profile = collection.update_one({"_id": ObjectId(profile_id)}, {"$set": update_fields})
    return updated_profile.modified_count


# Get user profile by ID
def get_user_profile(profile_id):
    return collection.find_one({"_id": ObjectId(profile_id)})


# Upload user profile picture
def upload_profile_picture(file: UploadFile):
    with open(file.filename, 'wb') as f:
        f.write(file.file.read())
    return file.filename

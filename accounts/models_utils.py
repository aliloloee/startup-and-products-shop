


def profile_directory_path (instance, filename) :
    file_type = filename.split('.')[1]
    return f"profiles/avatars/user_id_{instance.user.id}.{file_type}"
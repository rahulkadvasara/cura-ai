def verify_user_access(request_user_id, session_user_id):

    if str(request_user_id) != str(session_user_id):
        raise Exception("Unauthorized access attempt")
"""
Validation logic in this file
"""

avoid = [' ','(', ')', '{', '}', '[', ']', '|', '`', '¬', '¦', '!', '"', '£', '$', '%', '^', '&', '*', '"', '<', '>', ':', ';','#','~','_','-','+','=',',','@', '/', '\\']
def passwordValidation(password):
    """
    Validate The Password
    """
    if len(password) <= 7:
            return "password too short"
    for i in password:
        if i in avoid:
            return "'" + i + "'" + " is not allowed in password"
    return True

def usernameValidation(username):
    """
    Validate the Username
    """
    for i in username:
        if i in avoid:
                return "'" + i + "'" + " is not allowed in username"
    return True

# print(usernameValidation('bruh is username'))

# from libs import auth
# from functools import wraps

# def login_required(fn): #pragma: no cover
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         if auth.check_env():
#             exist = auth.get_env_values()
            
#             if exist['logged_in'] == 'True':
#                 return fn(*args, **kwargs)
#         else :
#             print("You are not logged in. \nEnter login -n Name to log in")
#     return wrapper


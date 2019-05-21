## USERZONE ENDPOINT

Userzone endpoint's function is to tie zone and its owner. This endpoint requires you to include your user id on headers requests

Headers:
```raw
"user-id" : user::user_id
```

### GET USERZONE

- path: /api/user/userzone
- method: Get
- response: application/json
- body: None
- roles: all
- usage: Get zone owned by your account



### INSERT USERZONE

- path: /api/user/userzone
- method: post
- response: application/json
- body: raw
- roles: all
- usage: Connecting you zone and your account

Body :
```raw
{
  "id_zone" : zone::id_zone
}
```



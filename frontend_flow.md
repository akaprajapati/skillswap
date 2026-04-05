# 🚀 SkillSwap Frontend Flow (Updated with Feed, Likes & Comments)

---

# 🔐 AUTH FLOW

## Register

POST `/auth/register`

```json
{
  "email": "user@test.com",
  "password": "123456",
  "name": "User One"
}
```

---

## Login

POST `/auth/login`

```json
{
  "email": "user@test.com",
  "password": "123456"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN"
}
```

👉 Store token and send in all requests:

```http
Authorization: Bearer <token>
```

---

# 👤 PROFILE / ONBOARDING

## Get Profile

GET `/me/`

---

## Update Profile

PUT `/me/?name=Anand&bio=Backend Dev`

---

## Onboarding Logic

If:

* bio is empty
* no skills

👉 Show onboarding screen

---

# 🎯 SKILLS FLOW

## Load Categories + Skills (MAIN API)

GET `/skills/category-with-skills`

---

## UI STRUCTURE

```
Category Dropdown
  → Skills (checkbox / chips)
```

---

## Add Skills

POST `/skills/offer`
POST `/skills/want`

---

## Remove Skills

DELETE `/skills/offer`
DELETE `/skills/want`

---

## Get User Skills

GET `/skills/user/{user_id}`

---

# 🏠 FEED (UPDATED)

## Get Feed

GET `/posts/`

Response:

```json
[
  {
    "id": 1,
    "user_id": 1,
    "content": "Hello world",
    "created_at": "...",
    "like_count": 5,
    "comment_count": 2,
    "comments": [
      {
        "id": 1,
        "user_id": 2,
        "content": "Nice post!",
        "created_at": "..."
      }
    ]
  }
]
```

---

## UI DESIGN

Each post card:

```
User Info
Post Content

❤️ Like Count
💬 Comment Count

[ Like Button ]
[ Comment Button ]

Comments Section (expandable)
```

---

# 📝 POST ACTIONS

## Create Post

POST `/posts/`

```json
{
  "content": "My first post"
}
```

---

## Like Post

POST `/posts/like/{post_id}`

---

## Comment on Post

POST `/posts/comment`

```json
{
  "post_id": 1,
  "content": "Nice!"
}
```

---

## Get Single Post

GET `/posts/{post_id}`

👉 Use for:

* Post detail page
* Full comments view

---

# 🧠 FRONTEND BEHAVIOR

---

## LIKE FLOW

```
Click Like
 → Call API
 → Update like_count instantly (optimistic UI)
```

---

## COMMENT FLOW

```
Open comment box
 → Submit comment
 → Append to UI list
 → Increase comment_count
```

---

## COMMENTS UI

```
Show first 2 comments
[ View All Comments ]
```

---

# 👥 FOLLOW SYSTEM

POST `/follow?user_id=2`
DELETE `/follow?user_id=2`

---

# 💘 MATCH SYSTEM

POST `/match/swipe?to_user_id=2&action=like`

---

# 🔔 NOTIFICATIONS

GET `/notifications/{user_id}`

POST `/notifications/read/{notif_id}`

---

# ⚡ WEBSOCKET

## Notifications

```
wss://your-app.onrender.com/ws/notifications/{user_id}
```

---

## Chat

```
wss://your-app.onrender.com/ws/chat/{match_id}/{user_id}
```

---

# 🎯 FULL APP FLOW

---

## AFTER LOGIN

```
Login
 → /me
   → incomplete → onboarding
   → else → dashboard
```

---

## ONBOARDING

```
Fill:
- Name
- Bio
- Offered skills
- Wanted skills
```

---

## DASHBOARD

```
Feed
 → Posts
 → Likes
 → Comments
 → Follow
 → Swipe
```

---

## PROFILE

```
Edit:
- Bio
- Skills
```

---

## NOTIFICATIONS

```
Real-time bell 🔔
```

---

# ⚠️ IMPORTANT RULES

* Always send Authorization header
* Skills are admin-controlled
* Use category-with-skills API
* Prevent duplicate likes

---

# 🎯 MVP STATUS

✔ Auth
✔ Profile
✔ Skills
✔ Feed
✔ Likes
✔ Comments
✔ Match
✔ Chat
✔ Notifications

---

# 🚀 NEXT (OPTIONAL)

* Pagination (important)
* Infinite scroll
* Unlike feature
* Replies to comments
* Profile pictures

---

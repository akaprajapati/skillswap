# 🚀 SkillSwap Frontend Flow (UI Integration Guide)

## 🔐 AUTH FLOW

### 1. Register

POST `/auth/register`

```json
{
  "email": "user@test.com",
  "password": "123456",
  "name": "User One"
}
```

---

### 2. Login

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

👉 Store token in:

* localStorage OR
* memory (preferred)

---

## 🔑 AUTH HEADER (IMPORTANT)

All protected routes require:

```http
Authorization: Bearer <token>
```

---

# 👤 PROFILE / ONBOARDING FLOW

## 3. Get Current User

GET `/me/`

Response:

```json
{
  "id": 1,
  "email": "user@test.com",
  "name": "User One",
  "bio": null,
  "offered_skills": [],
  "wanted_skills": []
}
```

---

## 🧠 LOGIC

If:

```text
bio == null OR skills empty
```

👉 Show **Onboarding Screen**

---

## 4. Update Profile

PUT `/me/?name=Anand&bio=Backend Developer`

---

# 🎯 SKILLS FLOW (MAIN UI)

## 5. Load Categories + Skills

GET `/skills/category-with-skills`

Response:

```json
[
  {
    "id": 1,
    "name": "Programming",
    "skills": [
      { "id": 1, "name": "Python" },
      { "id": 2, "name": "Java" }
    ]
  }
]
```

---

## 🧠 UI DESIGN

```
Category (Dropdown)
   ↓
List of skills (Checkbox / Chips)
```

---

## 6. Add Offered Skill

POST `/skills/offer`

```json
{
  "user_id": 1,
  "skill_id": 1
}
```

---

## 7. Add Wanted Skill

POST `/skills/want`

```json
{
  "user_id": 1,
  "skill_id": 2
}
```

---

## 8. Remove Skill

DELETE `/skills/offer`
DELETE `/skills/want`

---

## 9. Get User Skills

GET `/skills/user/{user_id}`

---

# 🏠 DASHBOARD / FEED

## 10. Get Feed

GET `/posts/`

---

## 11. Personalized Feed

GET `/posts/feed/personalized`

---

# 📝 POSTS

## Create Post

POST `/posts/`

```json
{
  "content": "Hello world"
}
```

---

## Like Post

POST `/posts/like/{post_id}`

---

## Comment

POST `/posts/comment`

```json
{
  "post_id": 1,
  "content": "Nice post!"
}
```

---

# 👥 FOLLOW SYSTEM

## Follow

POST `/follow?user_id=2`

## Unfollow

DELETE `/follow?user_id=2`

---

# 💘 MATCH SYSTEM (TINDER STYLE)

## Swipe

POST `/match/swipe?to_user_id=2&action=like`

Actions:

* like
* skip

---

# 🔔 NOTIFICATIONS

## Get Notifications

GET `/notifications/{user_id}`

---

## Mark as Read

POST `/notifications/read/{notif_id}`

---

# ⚡ WEBSOCKET (REAL-TIME)

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

# 🎯 FULL UI FLOW

## AFTER LOGIN

```
Login
 → /me
   → if incomplete → onboarding
   → else → dashboard
```

---

## ONBOARDING

```
1. Update name + bio
2. Select offered skills
3. Select wanted skills
4. Save → Dashboard
```

---

## DASHBOARD

```
- Feed (posts)
- Create post
- Like / comment
- Follow users
- Swipe profiles
```

---

## PROFILE PAGE

```
- View profile
- Edit bio
- Add/remove skills
```

---

## NOTIFICATIONS

```
- Real-time (WebSocket)
- Bell icon 🔔
```

---

# ⚠️ IMPORTANT NOTES

* Always send Authorization header
* Do NOT allow user to create skills
* Use category-with-skills API for UI
* Avoid duplicate skill calls

---

# 🎯 MVP COMPLETE

You now have:

✔ Auth
✔ Profile
✔ Skills system
✔ Feed
✔ Match
✔ Chat
✔ Notifications

---

# 🚀 NEXT (OPTIONAL)

* Profile picture upload
* Search users
* Skill-based recommendations
* UI animations

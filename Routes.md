# 📡 SkillSwap API Routes Documentation

This document contains all REST API routes, request payloads, and responses.

---

# 🌐 BASE URL

```
https://your-app.onrender.com
```

---

# 🔐 AUTH MODULE

---

## ✅ Register

**POST** `/auth/register`

### 📤 Payload

```json
{
  "email": "user1@test.com",
  "password": "123456",
  "name": "User One"
}
```

### 📥 Response

```json
{
  "message": "User created"
}
```

---

## ✅ Login

**POST** `/auth/login`

### 📤 Payload

```json
{
  "email": "user1@test.com",
  "password": "123456"
}
```

### 📥 Response

```json
{
  "access_token": "JWT_TOKEN"
}
```

---

# 🔑 AUTH HEADER (FOR ALL PROTECTED ROUTES)

```
Authorization: Bearer <JWT_TOKEN>
```

---

# 🧑‍🤝‍🧑 FOLLOW MODULE

---

## ✅ Follow User

**POST** `/follow?user_id=2`

### 📥 Response

```json
{
  "message": "Followed successfully"
}
```

---

## ❌ Unfollow User

**DELETE** `/follow?user_id=2`

### 📥 Response

```json
{
  "message": "Unfollowed"
}
```

---

## 👥 Get Followers

**GET** `/follow/followers/{user_id}`

### 📥 Response

```json
[
  { "user_id": 1 },
  { "user_id": 3 }
]
```

---

## ➡️ Get Following

**GET** `/follow/following/{user_id}`

### 📥 Response

```json
[
  { "user_id": 2 },
  { "user_id": 5 }
]
```

---

# 📝 POSTS MODULE

---

## ✅ Create Post

**POST** `/posts/`

### 📤 Payload

```json
{
  "content": "Hello world 🚀"
}
```

### 📥 Response

```json
{
  "message": "Post created"
}
```

---

## 📜 Get Feed

**GET** `/posts/`

### 📥 Response

```json
[
  {
    "id": 1,
    "user_id": 1,
    "content": "Hello world"
  }
]
```

---

## ❤️ Like Post

**POST** `/posts/like/{post_id}`

### 📥 Response

```json
{
  "message": "Post liked"
}
```

---

## 💬 Comment on Post

**POST** `/posts/comment`

### 📤 Payload

```json
{
  "post_id": 1,
  "content": "Nice post!"
}
```

### 📥 Response

```json
{
  "message": "Comment added"
}
```

---

## 🎯 Personalized Feed

**GET** `/posts/feed/personalized`

### 📥 Response

```json
[
  {
    "id": 2,
    "user_id": 2,
    "content": "From followed user"
  }
]
```

---

# 🔁 MATCH MODULE

---

## 👉 Swipe

**POST** `/match/swipe?to_user_id=2&action=like`

### 📥 Response (Normal)

```json
{
  "message": "Swipe recorded"
}
```

### 🎉 Response (Match Created)

```json
{
  "message": "🎉 Match created!",
  "match_id": 1
}
```

---

## 📄 Get Matches

**GET** `/match/user/{user_id}`

### 📥 Response

```json
{
  "id": 1,
  "email": "user@test.com"
}
```

---

# 💬 CHAT MODULE (REST for history if added later)

(Currently handled via WebSocket)

---

# 🔔 NOTIFICATIONS MODULE

---

## 📥 Get Notifications

**GET** `/notifications/{user_id}`

### 📥 Response

```json
[
  {
    "id": 1,
    "title": "New Follower",
    "message": "user1@test.com followed you",
    "is_read": false
  }
]
```

---

## ✅ Mark Notification as Read

**POST** `/notifications/read/{notif_id}`

### 📥 Response

```json
{
  "message": "Marked as read"
}
```

---

# 🧠 SKILLS MODULE

---

## ➕ Create Category

**POST** `/skills/category`

```json
{
  "name": "Programming"
}
```

---

## ➕ Create Skill

**POST** `/skills/`

```json
{
  "name": "Python",
  "category_id": 1
}
```

---

## 🎯 Offer Skill

**POST** `/skills/offer`

```json
{
  "user_id": 1,
  "skill_id": 1
}
```

---

## 🎯 Want Skill

**POST** `/skills/want`

```json
{
  "user_id": 1,
  "skill_id": 2
}
```

---

## 📜 List Skills

**GET** `/skills/`

---

## 👤 User Skills

**GET** `/skills/user/{user_id}`

```json
{
  "user": "User One",
  "offered": ["Python"],
  "wanted": ["Guitar"]
}
```

---

# 🔐 RBAC MODULE (ADMIN PANEL)

---

## ➕ Create Role

**POST** `/rbac/roles`

```json
{
  "name": "Admin"
}
```

---

## ➕ Create Permission

**POST** `/rbac/permissions`

```json
{
  "name": "create_post"
}
```

---

## 🔗 Assign Role

**POST** `/rbac/assign-role`

```json
{
  "user_id": 1,
  "role_id": 1
}
```

---

## 🔗 Assign Permission

**POST** `/rbac/assign-permission`

```json
{
  "role_id": 1,
  "permission_id": 1
}
```

---

## 👥 Get Users

**GET** `/rbac/users`

---

## 👤 Get User Details

**GET** `/rbac/users/{user_id}`

---

# ⚠️ COMMON ERRORS

---

## ❌ 401 Unauthorized

Token missing or invalid

## ❌ 403 Forbidden

User does not have permission

## ❌ 404 Not Found

Invalid ID

---

# 🎯 FINAL FEATURES COVERED

* Auth (JWT)
* RBAC
* Follow system
* Social feed
* Matchmaking
* Chat (WebSocket)
* Notifications (real-time + DB)
* Skills marketplace

---

# 🚀 NOTES FOR FRONTEND

* Always store JWT after login
* Use Authorization header
* Use WebSocket for real-time features
* Handle 403 for UI restrictions
* Implement retry for WebSocket reconnect

---

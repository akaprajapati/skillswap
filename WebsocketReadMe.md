# 🔌 WebSocket Integration Guide (SkillSwap Backend)

This document explains how to integrate real-time features (notifications & chat) with the backend.

---

# 🌐 BASE URL

```
https://your-app.onrender.com
```

---

# 🔔 NOTIFICATIONS (REAL-TIME)

## 📡 WebSocket Endpoint

```
wss://your-app.onrender.com/ws/notifications/{user_id}
```

## 📥 Example

```
wss://your-app.onrender.com/ws/notifications/2
```

## 📌 Behavior

* Automatically receives events:

  * New follower
  * Post liked
  * Comment added
  * Match created

## 📦 Payload

```json
{
  "title": "New Follower",
  "message": "user1@test.com started following you"
}
```

## 💻 Frontend Usage

```javascript
const socket = new WebSocket(
  `wss://your-app.onrender.com/ws/notifications/${userId}`
);

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  // Show toast / update UI
  console.log(data);
};
```

---

# 💬 CHAT (REAL-TIME)

## 📡 WebSocket Endpoint

```
wss://your-app.onrender.com/ws/chat/{match_id}/{user_id}
```

## 📥 Example

```
wss://your-app.onrender.com/ws/chat/1/2
```

---

## 📤 Send Message

```json
{
  "message": "Hello!",
  "receiver_id": 1
}
```

---

## 📥 Receive Message

```json
{
  "sender_id": 2,
  "message": "Hello!"
}
```

---

## 💻 Frontend Usage

```javascript
const socket = new WebSocket(
  `wss://your-app.onrender.com/ws/chat/${matchId}/${userId}`
);

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};

function sendMessage(msg, receiverId) {
  socket.send(JSON.stringify({
    message: msg,
    receiver_id: receiverId
  }));
}
```

---

# ⚠️ IMPORTANT NOTES

* Always use `wss://` (NOT `ws://`) in production
* Keep connection alive (do not close)
* Reconnect on disconnect
* Use user_id from logged-in user
* Chat only works if users are matched

---

# 🧪 TESTING

You can test WebSockets using:

* Postman (WebSocket tab)
* Browser console
* Frontend app

---

# 🎯 FEATURES SUPPORTED

* Real-time notifications
* Live chat messaging
* Event-driven updates

---

# 🚀 FUTURE IMPROVEMENTS

* Notification unread count
* Typing indicators (chat)
* Message delivery status
* Push notifications (mobile)

---

# 👨‍💻 Backend Contact

If any issue, contact backend dev with:

* Endpoint
* Payload
* Error logs

---

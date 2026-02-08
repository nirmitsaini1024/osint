# 🤖 Chatbot Usage Guide

## ✅ Fixed Issues

### 1. **Username Extraction**
- ✅ "Find all accounts of **kash**" → Now correctly extracts "kash" (not "all")
- ✅ Common words like "all", "them", "it", "name" are now ignored
- ✅ Smarter pattern matching with stop words

### 2. **Conversation Memory**
- ✅ The chatbot now remembers the last username you queried
- ✅ You can ask follow-up questions without repeating the username

---

## 💬 How to Use the Chatbot

### Example Conversation:

```
You: Find all accounts of kash
Bot: 🔍 Investigation Results for 'kash':
     Found 25 accounts...

You: is it suspicious?
Bot: 🧠 AI Risk Analysis for 'kash':  ← Remembers "kash"!
     Risk Score: 4.2/10...

You: show risk score
Bot: 📊 Risk Score Analysis for 'kash':  ← Still remembers!
     Overall Risk Score: 4.2/10...

You: generate report
Bot: 📝 Investigation Report for 'kash':  ← Remembers throughout!
```

---

## 📝 Query Examples

### Investigation (Find Accounts)
```
Find all accounts of elonmusk
Search for username alice123
Locate accounts for bob_smith
```

### Intelligence (AI Analysis)
```
Is elonmusk suspicious?
Which platform has highest risk?
Analyze threats
```
*Note: If you don't specify a username, it uses the last one from conversation*

### Analysis (Risk Scoring)
```
Show risk score for john_doe
Analyze profile
What's the risk level?
```

### Reporting (Generate Reports)
```
Generate investigation report for alice
Create summary
Summarize findings
```

---

## 🎯 Pro Tips

1. **Start with Investigation**:
   First ask: "Find all accounts of USERNAME"
   Then ask follow-ups without repeating the username

2. **Follow-up Questions Work**:
   ```
   You: Find all accounts of test123
   Bot: [Shows results]
   
   You: is it suspicious?        ← No need to repeat username!
   You: show risk score          ← Still remembers!
   You: generate report          ← Context maintained!
   ```

3. **Switch Users**:
   Just mention a new username in any query to switch context
   ```
   You: Find all accounts of user1
   Bot: [Results for user1]
   
   You: Find all accounts of user2  ← New context
   Bot: [Results for user2]
   
   You: is it suspicious?          ← Refers to user2 now
   ```

---

## 🔄 How to Apply Updates

### 1. Restart Backend
```bash
# In your backend terminal (Ctrl+C to stop first)
cd /home/nirmit/Downloads/work/kkkash/sherlock
source venv/bin/activate
python api.py
```

### 2. Restart Frontend (if needed)
```bash
# In your frontend terminal (Ctrl+C to stop first)
cd /home/nirmit/Downloads/work/kkkash/frontend
npm run dev
```

### 3. Hard Refresh Browser
- Press `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)
- Or clear browser cache

---

## ✅ Test It Works

Try this conversation:

1. **First query with username**:
   ```
   Find all accounts of test123
   ```
   Should show investigation results for "test123"

2. **Follow-up WITHOUT username**:
   ```
   is it suspicious?
   ```
   Should analyze "test123" (remembered from step 1)

3. **Another follow-up**:
   ```
   show risk score
   ```
   Should show risk score for "test123"

If all three work correctly, **conversation memory is working!** 🎉

---

## 🐛 Troubleshooting

### "Still extracting wrong username"
- Restart the backend
- Hard refresh browser (Ctrl+Shift+R)

### "Doesn't remember previous username"
- Make sure you restarted BOTH backend and frontend
- Clear browser cache
- Check that the first query includes a clear username

### "AI not working"
- Check `.env` file has: `GROQ_API_KEY=your_key_here`
- Restart backend
- Test: `curl http://localhost:8000/chatbot/status`

---

## 🎉 Enjoy Your Improved Chatbot!

Now you can have natural conversations without repeating usernames! 🚀



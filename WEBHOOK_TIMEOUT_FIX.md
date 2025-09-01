# Webhook Timeout Fix Guide

## Issue: "We couldn't deliver this payload: timed out"

This error occurs when GitHub's webhook delivery times out (10-second limit). I've implemented a fix to resolve this.

## 🔧 **Root Cause**
The timeout was happening because the webhook handler was trying to process everything synchronously, including:
- Database operations
- AI agent processing
- GitHub API calls

This caused the webhook to hang until timeout.

## ✅ **Fix Applied**

### **Immediate Response Pattern**
The webhook now responds immediately and processes everything in the background:

```python
@app.post("/webhooks/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    # Get webhook data
    body = await request.body()
    headers = dict(request.headers)
    event_type = headers.get("X-GitHub-Event")
    
    # Return immediate response (prevents timeout)
    asyncio.create_task(process_webhook_background(body, headers, db))
    return {
        "status": "success",
        "message": "Webhook received",
        "event_type": event_type
    }
```

### **Background Processing**
All heavy operations now run in the background:
- Database operations
- AI agent analysis
- GitHub API calls
- File processing

## 🧪 **Testing the Fix**

### **Step 1: Test Simple Webhook**
```bash
# Test the simple endpoint
curl -X POST "https://your-render-app.onrender.com/webhook-simple" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### **Step 2: Test Main Webhook**
```bash
# Test with GitHub-like headers
curl -X POST "https://your-render-app.onrender.com/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -d '{"action": "opened", "pull_request": {"number": 1}}'
```

### **Step 3: Check Logs**
Look for these messages in your Render logs:
```
🔍 Webhook received: pull_request
🔄 Processing webhook: pull_request
🚀 Starting AI review for PR ID: X
✅ AI review started for PR ID: X
✅ Webhook processing completed: pull_request
```

## 📊 **Expected Behavior**

### **Before Fix:**
- ❌ Webhook times out after 10 seconds
- ❌ GitHub shows "timed out" error
- ❌ No processing occurs

### **After Fix:**
- ✅ Webhook responds immediately (< 1 second)
- ✅ GitHub shows "200 OK" status
- ✅ Processing continues in background
- ✅ AI review runs asynchronously

## 🔍 **Monitoring**

### **Key Log Messages to Watch:**
```
✅ "🔍 Webhook received: X" - Webhook received
✅ "🔄 Processing webhook: X" - Background processing started
✅ "🚀 Starting AI review for PR ID: X" - AI review triggered
✅ "✅ AI review started for PR ID: X" - AI review running
✅ "✅ Webhook processing completed: X" - Processing finished
❌ "❌ Background processing failed: X" - Processing error
```

### **GitHub Webhook Delivery Status:**
- **200 OK**: Webhook processed successfully
- **Timeout**: Still timing out (should be fixed now)

## 🚨 **If Still Timing Out**

### **Emergency Fix:**
If the webhook is still timing out, temporarily use the simple endpoint:

1. **Change GitHub webhook URL** to:
   ```
   https://your-render-app.onrender.com/webhook-simple
   ```

2. **Test with simple endpoint** first
3. **Monitor logs** for any errors
4. **Switch back** to main endpoint once confirmed working

### **Debug Steps:**
1. **Check Render service status**
2. **Verify database connection**
3. **Check environment variables**
4. **Monitor resource usage**

## 📈 **Performance Improvements**

### **What Changed:**
1. **Immediate Response**: Webhook responds in < 1 second
2. **Background Processing**: Heavy operations run asynchronously
3. **Error Handling**: Errors don't cause timeouts
4. **Logging**: Better visibility into processing

### **Benefits:**
- ✅ No more timeouts
- ✅ Faster webhook delivery
- ✅ Better error handling
- ✅ Improved monitoring
- ✅ Scalable processing

## 🎯 **Next Steps**

1. **Deploy the fix** to your Render service
2. **Test with a simple PR** first
3. **Monitor logs** for successful processing
4. **Verify AI review** is working in background
5. **Check database** for stored data

## 📞 **Verification Checklist**

After deploying the fix, verify:

- [ ] **GitHub webhook delivery** shows "200 OK"
- [ ] **Render logs** show webhook received messages
- [ ] **Background processing** logs appear
- [ ] **AI review** starts for PRs
- [ ] **Database** contains PR and review data
- [ ] **No timeout errors** in GitHub

The webhook should now respond immediately and process everything in the background, eliminating the timeout issue!

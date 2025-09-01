# Webhook Timeout Troubleshooting Guide

## Issue: "We couldn't deliver this payload: timed out"

This error occurs when GitHub's webhook delivery times out (10-second limit). Here's how to diagnose and fix it.

## Root Cause Analysis

The timeout was caused by a **missing `handle_webhook` method** in the `GitHubWebhookHandler` class, which caused the webhook processing to fail silently.

## ✅ Fixes Applied

### 1. Added Missing Webhook Handler Method
- Added `handle_webhook()` method to `GitHubWebhookHandler` class
- Added `verify_signature_manual()` method for signature verification
- Proper error handling and logging

### 2. Optimized Webhook Processing
- Made webhook response immediate (AI review runs in background)
- Added better error logging
- Improved exception handling

### 3. Added Debug Endpoints
- `/webhook-test` - Test webhook endpoint accessibility
- `/db-test` - Test database connection
- `/health` - Check system health

## 🔍 How to Test the Fix

### 1. Test Webhook Endpoint
```bash
# Test if endpoint is accessible
curl "https://your-render-app.onrender.com/webhook-test"
```

### 2. Test Database Connection
```bash
# Test database connectivity
curl "https://your-render-app.onrender.com/db-test"
```

### 3. Test System Health
```bash
# Check overall system health
curl "https://your-render-app.onrender.com/health"
```

### 4. Monitor Logs
Check your Render logs for:
- ✅ "Webhook ping received" (for ping events)
- ✅ "Created new PR #X" or "Updated existing PR #X"
- ✅ "AI review task created for PR ID: X"
- ❌ Any error messages

## 🚀 Testing with Real PR

1. **Create a test repository** with the dummy files
2. **Set up webhook** in GitHub:
   ```
   URL: https://your-render-app.onrender.com/webhooks/github
   Content type: application/json
   Events: Pull requests
   Secret: (optional, but recommended)
   ```

3. **Create a PR** with changes to `test_python_file.py`

4. **Check webhook delivery** in GitHub:
   - Go to repository → Settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" tab
   - Should show "200 OK" status

5. **Verify database**:
   ```sql
   -- Check PR was stored
   SELECT * FROM pull_requests ORDER BY created_at DESC LIMIT 1;
   
   -- Check AI suggestions were created
   SELECT * FROM code_reviews ORDER BY created_at DESC LIMIT 5;
   ```

## 🔧 Common Issues & Solutions

### Issue 1: Webhook Still Timing Out
**Symptoms**: Still getting timeout errors
**Solutions**:
- Check Render logs for errors
- Verify database connection
- Ensure all environment variables are set

### Issue 2: No PR Data in Database
**Symptoms**: Webhook succeeds but no PR data stored
**Solutions**:
- Check webhook payload format
- Verify database permissions
- Check for SQL errors in logs

### Issue 3: AI Review Not Triggering
**Symptoms**: PR stored but no AI suggestions
**Solutions**:
- Check AI service configuration
- Verify GitHub API access
- Check custom rules file path

### Issue 4: Signature Verification Fails
**Symptoms**: "Invalid webhook signature" errors
**Solutions**:
- Set `GITHUB_WEBHOOK_SECRET` environment variable
- Or leave it empty to skip verification (not recommended for production)

## 📊 Monitoring & Debugging

### Key Log Messages to Watch For:
```
✅ "Webhook ping received" - Ping event successful
✅ "Created new PR #X" - PR stored successfully  
✅ "AI review task created for PR ID: X" - AI review triggered
✅ "Stored X suggestions in database" - AI suggestions saved
❌ "Webhook processing failed" - Webhook processing error
❌ "AI review trigger failed" - AI review failed (non-blocking)
```

### Database Queries for Verification:
```sql
-- Check recent PRs
SELECT id, title, repository, pr_number, created_at 
FROM pull_requests 
ORDER BY created_at DESC LIMIT 5;

-- Check AI suggestions
SELECT file_path, suggestion_type, severity, title 
FROM code_reviews 
ORDER BY created_at DESC LIMIT 10;

-- Check files
SELECT filename, status, additions, deletions 
FROM files 
ORDER BY created_at DESC LIMIT 5;
```

## 🚨 Emergency Fixes

If webhook is still failing:

1. **Temporarily disable AI review**:
   ```python
   # Comment out AI review trigger in main.py
   # asyncio.create_task(ai_review_service.process_pr_review(db, pr_id))
   ```

2. **Simplify webhook response**:
   ```python
   # Return simple success response
   return {"status": "success", "message": "Webhook received"}
   ```

3. **Check Render service status**:
   - Verify service is running
   - Check resource usage
   - Ensure no memory/CPU limits exceeded

## 📈 Performance Optimization

To prevent future timeouts:

1. **Database optimization**:
   - Use connection pooling
   - Optimize queries
   - Add indexes if needed

2. **Async processing**:
   - Keep webhook response fast
   - Move heavy processing to background
   - Use queues for AI review tasks

3. **Monitoring**:
   - Set up alerts for webhook failures
   - Monitor response times
   - Track AI review completion rates

## ✅ Success Criteria

Webhook is working correctly when:
- [ ] GitHub webhook delivery shows "200 OK"
- [ ] PR data is stored in database
- [ ] AI review suggestions are generated
- [ ] No timeout errors in GitHub webhook logs
- [ ] System logs show successful processing

## 📞 Next Steps

1. **Deploy the fixes** to your Render service
2. **Test with a simple PR** first
3. **Monitor logs** for any remaining issues
4. **Scale up testing** with more complex PRs
5. **Set up monitoring** for production use

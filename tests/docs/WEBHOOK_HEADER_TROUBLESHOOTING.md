# Webhook Header Troubleshooting Guide

## Issue: "Missing X-GitHub-Event header" (400 Error)

This error occurs when GitHub webhook requests don't include the required headers. Here's how to diagnose and fix it.

## 🔍 Root Cause Analysis

The 400 error indicates that your webhook endpoint is not receiving the expected GitHub headers. This can happen due to:

1. **Incorrect webhook configuration** in GitHub
2. **Network/proxy issues** between GitHub and your endpoint
3. **Header case sensitivity** issues
4. **Missing webhook secret** configuration

## ✅ Fixes Applied

### 1. Enhanced Header Debugging
- Added detailed header logging
- Made signature verification optional for testing
- Added flexible header name checking
- Created `/webhook-debug` endpoint for testing

### 2. More Flexible Header Handling
- Checks for both `X-GitHub-Event` and `x-github-event`
- Makes signature optional during testing
- Provides detailed error messages with available headers

## 🔧 How to Debug

### Step 1: Test the Debug Endpoint
```bash
# Test the debug endpoint to see what headers are being received
curl -X POST "https://your-render-app.onrender.com/webhook-debug" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"test": "data"}'
```

### Step 2: Check Render Logs
Look for these log messages:
```
🔍 Received webhook headers: ['content-type', 'user-agent', ...]
📋 Event type: pull_request
📋 Signature present: True/False
```

### Step 3: Verify GitHub Webhook Configuration
In your GitHub repository:
1. Go to **Settings** → **Webhooks**
2. Check your webhook configuration:
   - **URL**: `https://your-render-app.onrender.com/webhooks/github`
   - **Content type**: `application/json`
   - **Events**: `Pull requests` (or `Just the push event`)
   - **Secret**: (optional but recommended)

## 🚨 Common Issues & Solutions

### Issue 1: Webhook URL is Wrong
**Symptoms**: 404 errors or no requests received
**Solution**: 
- Verify the webhook URL is correct
- Ensure it points to `/webhooks/github` (not `/webhook/github`)

### Issue 2: Content Type Mismatch
**Symptoms**: Headers not received properly
**Solution**:
- Set Content type to `application/json` in GitHub webhook settings
- Don't use `application/x-www-form-urlencoded`

### Issue 3: Network/Proxy Issues
**Symptoms**: Headers stripped or modified
**Solution**:
- Check if you're behind a proxy that strips headers
- Verify Render service is accessible from GitHub

### Issue 4: Case Sensitivity
**Symptoms**: Headers exist but not detected
**Solution**:
- The fix now checks for both `X-GitHub-Event` and `x-github-event`
- Headers should be case-insensitive

## 🧪 Testing Steps

### 1. Test with Debug Endpoint
```bash
# Test with minimal headers
curl -X POST "https://your-render-app.onrender.com/webhook-debug" \
  -H "Content-Type: application/json" \
  -d '{"test": "ping"}'

# Test with GitHub-like headers
curl -X POST "https://your-render-app.onrender.com/webhook-debug" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -H "X-Hub-Signature-256: sha256=test" \
  -H "User-Agent: GitHub-Hookshot/test" \
  -d '{"zen": "test"}'
```

### 2. Test Main Webhook Endpoint
```bash
# Test with proper GitHub headers
curl -X POST "https://your-render-app.onrender.com/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -H "X-Hub-Signature-256: sha256=test" \
  -d '{"zen": "test"}'
```

### 3. Check GitHub Webhook Delivery
1. Go to your repository → **Settings** → **Webhooks**
2. Click on your webhook
3. Check **Recent Deliveries** tab
4. Look for:
   - ✅ **200 OK** status
   - ❌ **400 Bad Request** status
   - ❌ **Timeout** errors

## 📊 Expected Headers

GitHub should send these headers:
```
X-GitHub-Event: pull_request
X-Hub-Signature-256: sha256=...
Content-Type: application/json
User-Agent: GitHub-Hookshot/...
```

## 🔧 Manual Webhook Testing

### Test 1: Ping Event
```bash
curl -X POST "https://your-render-app.onrender.com/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen": "test"}'
```

### Test 2: Pull Request Event
```bash
curl -X POST "https://your-render-app.onrender.com/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -d '{"action": "opened", "pull_request": {"number": 1, "title": "test"}}'
```

## 🚨 Emergency Fixes

If webhook is still failing:

### 1. Temporarily Disable Header Checks
```python
# In main.py, comment out header checks temporarily
# if not event_type:
#     raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")
```

### 2. Use Debug Endpoint
- Point GitHub webhook to `/webhook-debug` instead
- Check what headers are actually being received
- Fix the main endpoint based on debug info

### 3. Check Render Service
- Verify service is running
- Check logs for any errors
- Ensure no firewall/proxy blocking headers

## 📈 Monitoring

### Key Log Messages to Watch:
```
✅ "Received webhook headers: [...]" - Headers received
✅ "Event type: pull_request" - Event type detected
✅ "Signature present: True" - Signature header present
❌ "Missing X-GitHub-Event header" - Header missing
❌ "Webhook processing failed" - Processing error
```

### GitHub Webhook Delivery Status:
- **200 OK**: Webhook processed successfully
- **400 Bad Request**: Header/validation error
- **500 Internal Server Error**: Server error
- **Timeout**: Request took too long

## ✅ Success Criteria

Webhook headers are working when:
- [ ] Debug endpoint shows all expected headers
- [ ] Main webhook endpoint returns 200 OK
- [ ] GitHub webhook delivery shows "200 OK"
- [ ] Logs show "Event type: pull_request"
- [ ] No "Missing X-GitHub-Event header" errors

## 📞 Next Steps

1. **Deploy the fixes** to your Render service
2. **Test with debug endpoint** first
3. **Check GitHub webhook configuration**
4. **Monitor logs** for header information
5. **Test with real PR** once headers are working

# Temp Models Cleanup System

## Overview

The temp models cleanup system automatically removes old STEP files from the `backend/temp_models` directory after 30 minutes to prevent disk space accumulation and maintain system performance.

## Features

- **Automatic Cleanup**: Files are automatically deleted after 30 minutes
- **Background Service**: Runs as a daemon thread, non-blocking
- **File Tracking**: Tracks when files are created for accurate cleanup
- **Manual Trigger**: API endpoints to manually trigger cleanup
- **Statistics**: Monitor cleanup service status and file counts
- **Graceful Shutdown**: Properly stops cleanup service on application exit

## Implementation Details

### Core Components

1. **TempModelsCleanupService** (`backend/langgraph_app.py`)
   - Manages the background cleanup thread
   - Tracks file creation timestamps
   - Handles file removal based on age

2. **CADModelGenerator Integration**
   - Automatically registers new files with cleanup service
   - Provides statistics and manual cleanup methods

3. **API Endpoints** (`backend/main.py`)
   - `/cleanup/stats` - Get cleanup service statistics
   - `/cleanup/manual` - Manually trigger cleanup

### Configuration

- **Cleanup Interval**: 30 minutes (configurable)
- **File Types**: `.step` files only
- **Directory**: `backend/temp_models/`

## API Endpoints

### GET /cleanup/stats

Get cleanup service statistics.

**Response:**
```json
{
  "status": "success",
  "cleanup_stats": {
    "total_files": 5,
    "tracked_files": 3,
    "cleanup_interval_minutes": 30,
    "service_running": true
  }
}
```

### POST /cleanup/manual

Manually trigger cleanup of old files.

**Response:**
```json
{
  "status": "success",
  "message": "Manual cleanup completed",
  "cleanup_stats": {
    "total_files": 2,
    "tracked_files": 1,
    "cleanup_interval_minutes": 30,
    "service_running": true
  }
}
```

## Usage Examples

### Check Cleanup Status
```bash
curl http://localhost:8000/cleanup/stats
```

### Manual Cleanup
```bash
curl -X POST http://localhost:8000/cleanup/manual
```

### Testing
```bash
cd backend
python test_cleanup.py
```

## File Lifecycle

1. **Creation**: When a CAD model is generated, the file is automatically registered with the cleanup service
2. **Tracking**: The service tracks the file's creation timestamp
3. **Cleanup**: After 30 minutes, the file is automatically deleted
4. **Manual**: Files can be manually cleaned up via API endpoint

## Monitoring

The cleanup service provides detailed logging:

- `🧹 Temp cleanup service initialized` - Service startup
- `📝 Registered file for cleanup` - New file registration
- `🧹 Cleanup check: no files older than X minutes found` - Regular checks
- `🗑️ Cleaned up old file` - File deletion
- `🛑 Cleanup service stopped` - Service shutdown

## Error Handling

- **File Access Errors**: Logged but don't stop the service
- **Thread Errors**: Service continues running with retry logic
- **Missing Files**: Gracefully handled during cleanup

## Docker Integration

The Dockerfile ensures:
- Proper directory creation with correct permissions
- Cleanup service starts automatically with the application
- Graceful shutdown handling

## Benefits

1. **Disk Space Management**: Prevents unlimited file accumulation
2. **Performance**: Keeps file system clean and fast
3. **Resource Efficiency**: Automatic cleanup without manual intervention
4. **Monitoring**: Visibility into cleanup operations
5. **Flexibility**: Manual cleanup option for immediate needs

## Configuration Options

To modify the cleanup interval, change the parameter in `CADModelGenerator.__init__()`:

```python
self.cleanup_service = TempModelsCleanupService(self.temp_dir, cleanup_interval_minutes=30)
```

## Troubleshooting

### Service Not Starting
- Check if the temp_models directory exists and has proper permissions
- Verify no other processes are using the directory

### Files Not Being Cleaned
- Check the cleanup service logs for errors
- Verify file timestamps are being set correctly
- Use manual cleanup to test functionality

### High Disk Usage
- Check if cleanup service is running: `GET /cleanup/stats`
- Trigger manual cleanup: `POST /cleanup/manual`
- Verify file permissions allow deletion 
from fastapi import FastAPI
import uvicorn
import redis
import json

app = FastAPI(title="Banking Cache Service", version="1.0.0")

# Redis connection (simplified for local testing)
# In a real scenario, this would connect to a Redis instance
cache_data = {}

@app.get("/")
async def root():
    return {"message": "Banking Cache Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "cache"}

@app.get("/cache/{key}")
async def get_cache(key: str):
    """Get value from cache"""
    return {"key": key, "value": cache_data.get(key, None)}

@app.post("/cache/{key}")
async def set_cache(key: str, value: dict):
    """Set value in cache"""
    cache_data[key] = value
    return {"message": f"Cache set for key: {key}"}

@app.delete("/cache/{key}")
async def delete_cache(key: str):
    """Delete value from cache"""
    if key in cache_data:
        del cache_data[key]
        return {"message": f"Cache deleted for key: {key}"}
    return {"message": f"Key {key} not found in cache"}

@app.get("/cache")
async def list_cache():
    """List all cache keys"""
    return {"keys": list(cache_data.keys())}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6379)


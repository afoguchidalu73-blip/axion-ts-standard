DEFAULT_NOISE_KEYS = {"timestamp", "request_id", "span_id", "latency"}

def strip_noise(payload, whitelist=None):
    if isinstance(payload, list):
        return [strip_noise(item, whitelist) for item in payload]
    if isinstance(payload, dict):
        return {k: strip_noise(v, whitelist) for k, v in payload.items() 
                if k not in DEFAULT_NOISE_KEYS or (whitelist and k in whitelist)}
    return payload
  

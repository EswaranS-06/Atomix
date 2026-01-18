# ATOMIX

## Atomic Target Orchestration for Mapping, Intelligence & eXploitation

### Why this works

- Atomic → tool steps are isolated and deterministic
- Target Orchestration → YAML-driven pipelines
- Mapping & Intelligence → recon-first philosophy
- Exploitation → future-ready (not just recon)

### This aligns perfectly with

> - Profiles
> - Docker runtime
> - Tool adapters
> - Structured output (future)

## Reference

```bash
whatweb https://example.com --log-json=/tmp/ww.json

nmap -sV --script vuln -oX /tmp/nmap.xml example.com

docker run --rm -it \
  -v $(pwd)/wordlists:/data/wordlists \
  recon

docker exec -it atomix-mongodb mongosh \
  -u atomix \
  -p atomixpass \
  --authenticationDatabase admin
#or
docker exec -it atomix-mongodb mongosh
use admin
db.auth("atomix", "atomixpass")



use atomix
db.scans.find().pretty()




curl -X POST http://127.0.0.1:8000/api/scans/ \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "profile": "default"}'

curl -X POST http://127.0.0.1:8000/api/scans/<scan_id>/queue/


uv run python manage.py shell
from scans.executor.runner import process_queued_scans
process_queued_scans()

```

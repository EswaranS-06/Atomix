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

whatweb https://example.com --log-json=/tmp/ww.json

nmap -sV --script vuln -oX /tmp/nmap.xml example.com

docker run --rm -it \
  -v $(pwd)/wordlists:/data/wordlists \
  recon

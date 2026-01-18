# ===============================
# Stage 1 — Builder
# ===============================
FROM alpine:3.19 AS builder

ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:/usr/local/bin:$PATH"
ENV GOBIN=/usr/local/bin

# -------------------------------
# Build dependencies
# -------------------------------
RUN apk add --no-cache \
    bash curl git ca-certificates \
    build-base linux-headers \
    python3 python3-dev py3-pip py3-virtualenv \
    go \
    ruby ruby-dev ruby-bundler ruby-json ruby-bigdecimal \
    perl perl-utils perl-net-ssleay \
    openssl openssl-dev libffi-dev \
    nmap nmap-scripts

# -------------------------------
# Python virtual environment
# -------------------------------
RUN python3 -m venv $VENV_PATH && \
    pip install --upgrade pip setuptools wheel

# -------------------------------
# Go-based tools
# -------------------------------
RUN go install github.com/OJ/gobuster/v3@v3.6.0 && \
    go install github.com/owasp-amass/amass/v4/...@v4.2.0 && \
    go install github.com/ffuf/ffuf/v2@v2.1.0

# -------------------------------
# Python-based tools
# -------------------------------
RUN pip install --no-cache-dir sublist3r

RUN git clone https://github.com/s0md3v/XSStrike.git /opt/tools/XSStrike && \
    pip install --no-cache-dir -r /opt/tools/XSStrike/requirements.txt

RUN git clone https://github.com/sqlmapproject/sqlmap.git /opt/tools/sqlmap

# -------------------------------
# Ruby-based tool: WhatWeb (vendored gems)
# -------------------------------
RUN git clone https://github.com/urbanadventurer/WhatWeb.git /opt/tools/whatweb && \
    cd /opt/tools/whatweb && \
    bundle config set without 'development test' && \
    bundle config set path 'vendor/bundle' && \
    bundle install

# -------------------------------
# Perl-based tool: Nikto
# -------------------------------
RUN git clone https://github.com/sullo/nikto.git /opt/tools/nikto

# -------------------------------
# Builder sanity checks
# -------------------------------
RUN python --version && \
    gobuster version && \
    ffuf -V && \
    amass -version || true


# ===============================
# Stage 2 — Runtime (Hardened)
# ===============================
FROM alpine:3.19

LABEL maintainer="Recon Automation Project"
LABEL description="Hardened Web Recon Engine Runtime"

ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:/usr/local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# ---- WhatWeb / Bundler environment ----
ENV GEM_HOME=/opt/tools/whatweb/vendor/bundle
ENV GEM_PATH=/opt/tools/whatweb/vendor/bundle
ENV BUNDLE_GEMFILE=/opt/tools/whatweb/Gemfile

# -------------------------------
# Runtime dependencies
# -------------------------------
RUN apk add --no-cache \
    bash curl ca-certificates \
    python3 \
    ruby ruby-bundler ruby-json ruby-bigdecimal \
    perl perl-net-ssleay \
    nmap nmap-scripts \
    openssl libffi \
    jq

# ---- CRITICAL FIX: install bundler gem ----
RUN gem install bundler --no-document

# -------------------------------
# Copy runtime artifacts
# -------------------------------
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/tools /opt/tools
COPY --from=builder /usr/local/bin/gobuster /usr/local/bin/gobuster
COPY --from=builder /usr/local/bin/ffuf /usr/local/bin/ffuf
COPY --from=builder /usr/local/bin/amass /usr/local/bin/amass

# -------------------------------
# Tool entrypoints
# -------------------------------
RUN ln -s /opt/tools/nikto/program/nikto.pl /usr/local/bin/nikto && \
    cat <<'EOF' > /usr/local/bin/whatweb
#!/bin/sh
cd /opt/tools/whatweb || exit 1
exec bundle exec ruby whatweb "$@"
EOF
RUN chmod +x /usr/local/bin/whatweb

RUN cat <<'EOF' > /usr/local/bin/sqlmap
#!/bin/sh
exec python3 /opt/tools/sqlmap/sqlmap.py "$@"
EOF
RUN chmod +x /usr/local/bin/sqlmap

    # printf '#!/bin/sh\ncd /opt/tools/whatweb || exit 1\nexec bundle exec ruby whatweb \"$@\"\n' \
    #     > /usr/local/bin/whatweb && chmod +x /usr/local/bin/whatweb

# -------------------------------
# Permissions hardening
# -------------------------------
RUN chown -R root:root /opt/tools && \
    chmod -R 755 /opt/tools

# -------------------------------
# Non-root execution
# -------------------------------
RUN adduser -D recon && \
    mkdir -p /data && \
    chown -R recon:recon /data

USER recon
WORKDIR /opt/recon

CMD ["/bin/bash"]

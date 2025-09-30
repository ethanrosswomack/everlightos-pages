#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/ethanrosswomack/everlightos.git"
REPO_DIR="/bridgeops_src"
TARGET_SUBPATH="Amazon_RME_BridgeOps"
APP_PORT="8081"

echo "Preparing runtime..."

# clone or update repo
if [ -d "$REPO_DIR" ]; then
  echo "Updating existing repo..."
  cd "$REPO_DIR" && git pull || true
else
  echo "Cloning repo..."
  git clone --depth 1 "$REPO_URL" "$REPO_DIR" || true
fi

TARGET_PATH="$REPO_DIR/$TARGET_SUBPATH"
echo "Looking for BridgeOps at $TARGET_PATH"

# Try common entrypoints
cd "$TARGET_PATH" || {
  echo "BridgeOps folder not present, will run fallback mock server."
  python /app/proxy_app.py &
  wait -n
  exit 0
}

echo "Inside BridgeOps path. Listing files:"
ls -la

# If there's a run.sh or start.sh run it
if [ -x "$TARGET_PATH/run.sh" ]; then
  echo "Found run.sh, executing..."
  (cd "$TARGET_PATH" && ./run.sh) &
  sleep 1
elif [ -x "$TARGET_PATH/start.sh" ]; then
  echo "Found start.sh, executing..."
  (cd "$TARGET_PATH" && ./start.sh) &
  sleep 1
# Python common entrypoints
elif [ -f "$TARGET_PATH/app.py" ]; then
  echo "Found app.py, launching with python on port $APP_PORT..."
  (cd "$TARGET_PATH" && python app.py &) || true
  sleep 1
elif [ -f "$TARGET_PATH/main.py" ]; then
  echo "Found main.py, launching..."
  (cd "$TARGET_PATH" && python main.py &) || true
  sleep 1
elif [ -f "$TARGET_PATH/wsgi.py" ]; then
  echo "Found wsgi.py, launching with gunicorn..."
  (cd "$TARGET_PATH" && pip install gunicorn && gunicorn -b 0.0.0.0:$APP_PORT wsgi:app &) || true
  sleep 1
else
  echo "No obvious entrypoint found in BridgeOps. Running fallback mock server."
  python /app/proxy_app.py &
  sleep 1
fi

# Start proxy app which listens on 8080 and forwards to APP_PORT
python /app/proxy_app.py

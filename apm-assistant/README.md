APM Assistant — proxy to BridgeOps repo
======================================

This container will attempt to clone (or update) your GitHub repo and locate the folder:
  Amazon_RME_BridgeOps

It tries common entrypoints inside that folder (run.sh, start.sh, app.py, main.py, wsgi.py).
If it finds something runnable, it will start it on port 8081 and then run a proxy on port 8080
that forwards /apm-assistant/* requests to the BridgeOps app. If no runnable entrypoint is found,
the container serves a fallback mock response for demo purposes.

Build & run locally:
  docker-compose up --build

Notes:
  - Ensure the container can reach github.com (network access) and that the repository is public or
    the container has credentials to access it.
  - If your BridgeOps app needs extra system packages, adjust the Dockerfile or provide a Dockerfile
    inside your repo's Amazon_RME_BridgeOps folder and modify start.sh to use it.
  - For production, build a dedicated image for the BridgeOps app and deploy to ECS/Cloud Run, then
    point the proxy or worker to that stable endpoint.

Configuration (environment variables):
  - BRIDGE_PORT: Port where the BridgeOps app will run (default 8081)
  - TARGET_SUBPATH: Change path inside cloned repo if different

Troubleshooting:
  - Logs: use docker-compose logs -f apm-assistant
  - If cloning fails, ensure git is installed and network outbound to github.com is allowed.

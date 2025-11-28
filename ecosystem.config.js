module.exports = {
  apps: [
    {
      name: "fastapi",
      script: "./venv/bin/uvicorn",
      args: "app.main:app --host 0.0.0.0 --port 8001 --reload",
      cwd: "/root/voice-auth-microservice",
      interpreter: "none",
      env: {
        PYTHONPATH: "/root/voice-auth-microservice"
      },
      max_restarts: 10,
      min_uptime: "10s"
    }
  ]
}
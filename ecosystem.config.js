module.exports = {
  apps: [
    {
      name: "fastapi",
      script: "uvicorn",
      args: ["app.main:app", "--host", "0.0.0.0", "--port", "8001"],
      interpreter: "none"
    }
  ]
}
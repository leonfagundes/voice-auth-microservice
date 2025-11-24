module.exports = {
  apps: [
    {
      name: "fastapi",
      script: "uvicorn",
      args: ["main:app", "--host", "0.0.0.0", "--port", "8001"],
      interpreter: "none"
    }
  ]
}
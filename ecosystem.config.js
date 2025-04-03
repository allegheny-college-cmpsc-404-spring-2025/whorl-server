module.exports = {
  apps: [{
    name: "whorl-server",
    interpreter: "./.venv/bin/python",
    script: 'src/manage.py',
    args: 'runserver 0.0.0.0:8000',
    ignore_watch: ["src/logs"],
    watch: '.'
  },
  {
    name: "prometheus",
    script: "../../usr/bin/prometheus",
    args: "--config.file=prometheus.yml"
  }
  ]
};

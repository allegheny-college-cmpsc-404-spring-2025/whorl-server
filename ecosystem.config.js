module.exports = {
  apps: [{
    name: "whorl-server",
    interpreter: "./.venv/bin/python",
    script: 'src/manage.py',
    args: 'runserver 0.0.0.0:8080',
    watch: '.'
  },
  {
    name: "prometheus",
    script: "usr/bin/prometheus",
    args: "--config.file=prometheus.yml"
  }
  ]
};

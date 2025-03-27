module.exports = {
  apps : [{
    name: "whorl-server",
    interpreter: "./.venv/bin/python",
    script: 'src/manage.py',
    args:'runserver 0.0.0.0:8080 --exclude "*.log"',
    watch: '.'
  }],
};

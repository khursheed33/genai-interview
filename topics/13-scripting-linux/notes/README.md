# Scripting and Linux Notes

## Shell
Pipelines compose small programs. Quote arguments, check exit codes, and prefer machine-readable output. grep filters text, sed transforms streams, awk processes fields, and jq processes JSON.

## Linux operations
Understand permissions, chmod/chown, users/groups, umask, processes, signals, file descriptors, environment variables, and standard streams. Use ps, top, kill, lsof, df, du, and /proc for diagnosis.

## Remote and automation
SSH provides secure remote access; rsync efficiently synchronizes files. Make standardizes commands, cron schedules simple jobs, systemd manages services, and Ansible performs declarative idempotent configuration. Use Python or PowerShell when shell scripting becomes difficult to maintain.

## Practice
Build a log-processing pipeline, write a robust Bash script with cleanup, diagnose CPU/disk pressure, perform an rsync backup, create a systemd service, and write an idempotent Ansible task.
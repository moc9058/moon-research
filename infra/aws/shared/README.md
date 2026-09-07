# Shared research VM

Status: **not deployed**

This will be the default Linux VM for experiments across multiple papers.
Paper-specific code and documentation remain under `papers/<paper>/`.

## Decisions required before provisioning

- AWS region and availability requirements
- CPU architecture and initial instance type
- root and data volume sizes
- operating system and AMI strategy
- Systems Manager access and IAM role
- outbound network requirements
- automatic stop schedule and budget threshold
- backup and persistence policy

## Lifecycle contract

The eventual implementation must expose and document:

```text
deploy   create or update the shared environment
connect  open an authenticated Session Manager session
status   show state, type, tags, and relevant cost information
stop     stop compute while preserving the environment
destroy  remove the stack after explicit confirmation
```

No command in this directory should silently create expensive resources or
make `destroy` an alias of `stop`.

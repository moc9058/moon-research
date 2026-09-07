# AWS compute

No AWS instance is currently provisioned by this repository.

The default design uses one shared VM for many papers. A paper may own a
dedicated environment when its OS, architecture, accelerator, kernel, network,
or isolation requirements differ.

```text
infra/aws/shared/                    # default shared VM
papers/<paper>/infra/aws/            # optional dedicated environment
```

## Rules

- Define resources with IaC before deployment.
- Document deployment, connection, status, stop, and destroy commands.
- Prefer Systems Manager Session Manager over a public SSH port.
- Tag resources with at least `Project=moon-research`, `Environment`, and
  `ManagedBy`.
- Use instance roles and local AWS profiles; never store credentials in Git.
- Keep `stop` separate from `destroy`. Stopped instances can still incur
  EBS and related charges.
- Do not deploy, replace, terminate, or destroy resources without an explicit
  user request.

Never commit access keys, secret keys, session tokens, private keys, account
IDs, instance IDs, Terraform state, CDK output, or private network details.

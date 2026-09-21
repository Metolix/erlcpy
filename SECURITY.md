# Security

Security issues in prcpy should be reported privately. Please do not open a public issue for a vulnerability before the maintainer has had a chance to investigate it.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting or Security Advisory workflow for this repository if it is available. If private reporting is not available, contact the repository maintainer privately through GitHub.

Include:
- A clear description of the issue.
- The affected version or commit.
- Steps to reproduce the problem.
- A minimal proof of concept where safe.
- The security impact.
- Any suggested mitigation.

Do not include real ER:LC server keys, global API keys, webhook secrets, access tokens, or other credentials in a report.

If a credential is accidentally exposed, rotate or revoke it immediately through the service that issued it before continuing the investigation.

## Credential handling

Treat ER:LC server keys, global API keys, webhook verification keys, and other integration credentials as secrets.

Recommended practices:
- Load credentials from environment variables or a dedicated secret manager.
- Never commit credentials to Git.
- Never put credentials in examples, documentation, tests, issue reports, or pull requests.
- Do not log request headers or full authenticated requests.
- Do not expose server keys in client-side applications.
- Rotate credentials if they may have been exposed.
- Give deployed applications only the credentials and permissions they actually need.

## Webhook verification

Applications receiving ER:LC webhooks should verify signatures before processing an event.

Do not treat a webhook payload as trusted merely because it reached your endpoint. Verify the signature against the raw request body before parsing or acting on the event.

Keep webhook verification keys private and fail closed when verification cannot be completed.

## Dependencies

Keep third-party dependencies reasonably current and review security advisories affecting supported Python and dependency versions.

Pull requests that change dependencies should explain why the dependency is needed and keep the dependency surface as small as practical.

## Security expectations

Security-sensitive data should not leak through exceptions, logs, test output, debug output, documentation, or CI artifacts.

Tests should use fake credentials and synthetic server data.

## Scope

This policy covers the prcpy package and the repository's maintained code, tests, examples, documentation, and CI configuration.

Vulnerabilities in ER:LC itself, Discord, Roblox, GitHub, or other external services should be reported to the relevant service rather than through this repository.

## Disclosure

Please allow reasonable time for investigation and remediation before publicly disclosing a vulnerability. Security fixes may be released before detailed technical information is published.

Thank you for helping keep prcpy and projects built with it secure.

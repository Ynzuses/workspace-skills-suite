# Contributing to Workspace Skills Suite

Use GitHub Issues for reproducible bugs, installation questions, documentation gaps, and focused proposals. Discuss a large redesign before submitting it so Skill ownership and scope can be reviewed.

## Making a change

1. Work from a checkout of this repository and change the owning Skill or documentation. Preserve complete Skill directories, stable IDs, sibling dependencies, and the declared group scope.
2. Keep public documentation and instructions in English. Use synthetic examples; exclude private documents, credentials, personal paths, unpublished results, and material you cannot redistribute.
3. Run the affected helper tests and applicable checks described in [VALIDATION.md](VALIDATION.md). Review frontmatter, referenced files, behavior boundaries, and installation after a packaging change. Check the actual host before claiming agent discovery, native application acceptance, or a live connection.
4. Explain the problem, resulting behavior, and validation in the pull request. State skipped or unavailable checks and preserve existing component attribution and licenses.

Instructions should improve a recognizable task without expanding user authorization or bypassing the host's permissions. Prefer a focused change with a realistic reproducer over additional universal rules. Changes to runtime behavior need appropriate behavioral evidence; a static check is not proof of future agent compliance.

## Reporting a problem

Include the release, Skill ID, agent and CLI versions, operating system, installation method, expected behavior, and actual behavior. Reduce the issue to a synthetic prompt or fixture. Do not place exploitable details or exposed secrets in a public issue; use the repository's private security reporting channel where available.

By submitting material, you confirm that you can contribute it under this repository's [Apache-2.0 license](LICENSE), while identifying any separately licensed component.

# Contributing

Thanks for improving VincentLogan Skills. Please use Issues for bugs, feature proposals, and questions; use pull requests for changes.

## Before opening a pull request

1. Keep each change focused on one Skill or repository concern.
2. Never commit courseware, personal notes, `.env` files, API keys, tokens, passwords, or other private material.
3. For a new Skill, add a directory named with lowercase letters, digits, and hyphens. It must contain a valid `SKILL.md` with `name` and `description` frontmatter.
4. Include only genuinely needed support files: deterministic helpers in `scripts/`, on-demand guidance in `references/`, and output assets in `assets/`.
5. Add or update `requirements.txt` whenever a script introduces a Python dependency.
6. Update the root `README.md` and create or refresh `dist/<skill-name>.zip` for a user-installable release.

## Quality checklist

- The Skill preserves user intent and clearly states input, output, and failure behavior.
- Scripts validate their command-line arguments and do not write outside the intended output location.
- Scripts do not contain credentials or hard-coded personal paths.
- Run the relevant script checks and validate the Skill before submitting.
- Describe the source material and verification performed in the pull request.

## Pull-request process

Fork the repository, create a branch, and open a pull request against `main`. Do not push directly to `main`; maintainers review pull requests before merging.

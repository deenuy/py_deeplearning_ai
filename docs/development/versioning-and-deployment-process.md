# Versioning and Deployment Process

## Version Numbering

We use Semantic Versioning (SemVer) for our version numbers: MAJOR.MINOR.PATCH

1. MAJOR version for incompatible API changes,
2. MINOR version for adding functionality in a backwards-compatible manner,
3. PATCH version for backwards-compatible bug fixes.

## Version Changes

1. **Production Releases**:
    - The version number changes only for production releases.
    - This ensures that each production release has a unique, traceable version number.

2. **Development and Staging**:
    - Use the next planned version number with a suffix:
        - Development: `2.1.0-dev.1`, `2.1.0-dev.2`, etc.
        - Staging: `2.1.0-rc.1`, `2.1.0-rc.2`, etc. (rc = Release Candidate)

3. **User Acceptance Testing (UAT)**:
    - Use release candidate versions: `2.1.0-rc.1`, `2.1.0-rc.2`, etc.

## Deployment Process for Different Environments

### Development Deployments

1. **Frequency**: Continuous, as features are developed.
2. **Version**: `MAJOR.MINOR.PATCH-dev.X`
3. **Process**:
    - Developers push to feature branches.
    - Automated tests run on each push.
    - Upon successful tests, auto-deploy to dev environment.
    - Update version in code to `MAJOR.MINOR.PATCH-dev.X`

### Staging Deployments

1. **Frequency**: After feature completion or on a regular schedule (e.g., weekly).
2. **Version**: `MAJOR.MINOR.PATCH-rc.X`
3. **Process**:
    - Merge feature branches to `develop`.
    - Run comprehensive tests.
    - Upon successful tests, auto-deploy to staging.
    - Update version in code to `MAJOR.MINOR.PATCH-rc.X`

### User Acceptance Testing (UAT)

1. **Frequency**: Before each production release.
2. **Version**: `MAJOR.MINOR.PATCH-rc.X` (same as staging)
3. **Process**:
    - Deploy latest staging version to UAT environment.
    - Notify UAT team to begin testing.
    - Collect and address feedback.
    - If changes are required, increment rc number and repeat.

### Production Release

1. **Frequency**: Based on release schedule or as needed.
2. **Version**: `MAJOR.MINOR.PATCH`
3. **Process**:
    - Final approval after successful UAT.
    - Remove `-rc.X` suffix from version number.
    - Create a release branch.
    - Deploy to production.
    - Tag the release in git.

## Version Control Workflow

1. **Feature Branches**: `feature/description`
    - Used for development, merged to `develop`.

2. **Develop Branch**:
    - Main integration branch.
    - Contains latest delivered development changes.
    - Version: `MAJOR.MINOR.PATCH-dev.X`

3. **Release Branches**: `release/MAJOR.MINOR.PATCH`
    - Created from `develop` for release preparation.
    - Version: `MAJOR.MINOR.PATCH-rc.X`

4. **Main Branch**:
    - Reflects the latest production release.
    - Version: `MAJOR.MINOR.PATCH`

5. **Hotfix Branches**: `hotfix/description`
    - Created from `main` for emergency fixes.
    - Increment PATCH version.

## Version Update Process

1. **Development**:
    - Update version in configuration files after each merge to `develop`.
    - Increment the `-dev.X` number.

2. **Staging/RC**:
    - Update version when creating a release branch.
    - Use `-rc.1` for the first release candidate.

3. **Production**:
    - Remove `-rc.X` suffix for final release.
    - Update CHANGELOG.md with all changes.

## Automation

- Use GitHub Actions or similar CI/CD tool to automate version updates and deployments.
- Implement checks to ensure version numbers are correctly incremented.

## Communication

- Clearly communicate version numbers in release notes and deployment notifications.
- Maintain a publicly accessible version history or changelog.


## This approach provides several benefits:

* Traceability: Each environment has a clear, unique version number.
* Clarity: The version number immediately indicates which environment it's for and how close it is to release.
* Flexibility: It allows for multiple release candidates and development versions without confusion.
* Consistency: Follows SemVer principles while accommodating different environments.
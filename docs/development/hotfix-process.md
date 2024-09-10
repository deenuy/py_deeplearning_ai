# Hotfix Process

This document outlines the step-by-step process for implementing and deploying a hotfix in our production environment.

## Process Flow

1. **Hotfix Request via IBM-Jazz**
    - A bug is reported and a IBM-Jazz ticket is created for a hotfix.

2. **Create Hotfix Branch**
    - From the `main` branch, create a new hotfix branch:
      ```
      git checkout main
      git pull
      git checkout -b hotfix-v1.2.1
      ```

3. **Implement Fix**
    - Developer implements the fix in the hotfix branch.
    - Commit changes:
      ```
      git add .
      git commit -m "Fix: Description of the fix (IBM-Jazz-1234)"
      ```

4. **Run Local Tests**
    - Developer runs local unit and integration tests:
      ```
      pytest
      ```

5. **Push Hotfix Branch**
    - Push the hotfix branch to the remote repository:
      ```
      git push -u origin hotfix-v1.2.1
      ```

6. **GitHub Actions Triggered**
    - Pushing to a `hotfix-*` branch automatically triggers the GitHub Actions workflow.
    - Automated tests are run on the hotfix branch.

7. **Create Pull Request**
    - If automated tests pass, developer creates a pull request from `hotfix-v1.2.1` to `main`.
    - Include a description of the changes and reference the IBM-Jazz ticket.

8. **Code Review**
    - Team reviews the code changes.
    - If changes are requested, developer makes updates and pushes again, triggering another GitHub Actions run.

9. **Merge to Main Branch**
    - Once approved, the changes are merged into the main branch.
    - This can be done through the GitHub UI or command line:
      ```
      git checkout main
      git merge --no-ff hotfix-v1.2.1
      git push origin main
      ```

10. **GitHub Actions Triggered**
    - Merging to `main` triggers another GitHub Actions workflow run.

11. **Update Changelog**
    - GitHub Actions updates `CHANGELOG.md` with the hotfix details:
      ```markdown
      ## [1.2.1] - 2023-06-15
      ### Fixed
      - Fixed issue with data processing in edge cases (IBM-Jazz-1234)
      ```

12. **Bump Version Number**
    - GitHub Actions updates version number in relevant files (e.g., `setup.py`, `__init__.py`) to 1.2.1

13. **Create Release Tag**
    - GitHub Actions creates a new git tag:
      ```
      git tag -a v1.2.1 -m "Hotfix 1.2.1"
      git push origin v1.2.1
      ```

14. **Deploy to Staging**
    - GitHub Actions deploys to staging environment.
    - This step is automated in the CI/CD pipeline.

15. **Run Integration Tests**
    - GitHub Actions runs full integration test suite in staging.
    - This step is automated in the CI/CD pipeline.

16. **Deploy to Production**
    - If staging tests pass, GitHub Actions deploys to production.
    - This step is automated in the CI/CD pipeline.

17. **Monitor Application**
    - Team closely monitors application metrics and logs for any issues.
    - Use monitoring tools to ensure the fix resolves the issue without introducing new problems.

18. **Merge Hotfix to Develop**
    - Developer merges the hotfix to `develop`:
      ```
      git checkout develop
      git merge main
      git push origin develop
      ```

19. **Close IBM-Jazz Ticket**
    - Update the IBM-Jazz ticket with resolution details.
    - Include links to relevant pull requests and commits.
    - Close the ticket.

## Notes

- Always ensure that the hotfix branch is created from the latest `main` branch.
- Communication is key. Keep the team informed about the progress of the hotfix.
- If any issues arise during the process, especially after deployment, be prepared to rollback the changes.
- After the hotfix is complete, conduct a post-mortem to identify any process improvements.

## GitHub Actions Workflow

Our GitHub Actions workflow (`ci-cd.yml`) automates several steps in this process, including:
- Running automated tests
- Updating the changelog
- Bumping the version number
- Creating release tags
- Deploying to staging and production

Refer to the `.github/workflows/ci-cd.yml` file for the exact configuration of our CI/CD pipeline.
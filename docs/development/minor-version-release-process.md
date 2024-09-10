# Minor Version Release Process

This document outlines the step-by-step process for implementing and deploying a minor version release in our production environment.

## Process Flow

1. **Release Planning**
    - Plan the features and improvements for the minor release.
    - Create a milestone in JIRA to track all related issues.

2. **Create Release Branch**
    - From the `develop` branch, create a new release branch:
      ```
      git checkout develop
      git pull
      git checkout -b release-v1.3.0
      ```

3. **Implement Features and Fixes**
    - Developers implement planned features and fixes in the release branch.
    - Each feature/fix should have its own commit:
      ```
      git add .
      git commit -m "Feature: Description of the feature (JIRA-1234)"
      ```

4. **Run Local Tests**
    - Developers run local unit and integration tests for each feature:
      ```
      pytest
      ```

5. **Push Release Branch**
    - Push the release branch to the remote repository:
      ```
      git push -u origin release-v1.3.0
      ```

6. **GitHub Actions Triggered**
    - Pushing to a `release-*` branch automatically triggers the GitHub Actions workflow.
    - Automated tests are run on the release branch.

7. **Create Pull Request**
    - Create a pull request from `release-v1.3.0` to `main`.
    - Include a description of all changes and reference relevant JIRA tickets.

8. **Code Review**
    - Team conducts a thorough review of all changes in the release.
    - If changes are requested, developers make updates and push again, triggering another GitHub Actions run.

9. **Update Changelog**
    - Update `CHANGELOG.md` with details of the new release:
      ```markdown
      ## [1.3.0] - 2023-06-30
      ### Added
      - New feature X (JIRA-1234)
      - New feature Y (JIRA-1235)
      
      ### Changed
      - Improved performance of Z (JIRA-1236)
      
      ### Fixed
      - Bug in feature W (JIRA-1237)
      ```

10. **Bump Version Number**
    - Update version number in relevant files (e.g., `setup.py`, `__init__.py`) to 1.3.0

11. **Final Testing**
    - Conduct thorough testing of all new features and changes.
    - This may include manual testing in addition to automated tests.

12. **Merge to Main Branch**
    - Once approved and tested, merge the release branch into `main`:
      ```
      git checkout main
      git merge --no-ff release-v1.3.0
      git push origin main
      ```

13. **GitHub Actions Triggered**
    - Merging to `main` triggers another GitHub Actions workflow run.

14. **Create Release Tag**
    - GitHub Actions creates a new git tag:
      ```
      git tag -a v1.3.0 -m "Release 1.3.0"
      git push origin v1.3.0
      ```

15. **Deploy to Staging**
    - GitHub Actions deploys to staging environment.
    - This step is automated in the CI/CD pipeline.

16. **Run Integration Tests**
    - GitHub Actions runs full integration test suite in staging.
    - This step is automated in the CI/CD pipeline.

17. **Deploy to Production**
    - If staging tests pass, GitHub Actions deploys to production.
    - This step is automated in the CI/CD pipeline.

18. **Monitor Application**
    - Team closely monitors application metrics and logs for any issues.
    - Use monitoring tools to ensure new features work as expected and no regressions occur.

19. **Merge Release to Develop**
    - Merge the release changes back to `develop`:
      ```
      git checkout develop
      git merge main
      git push origin develop
      ```

20. **Close JIRA Milestone**
    - Update and close all JIRA tickets associated with the release.
    - Close the release milestone in JIRA.

21. **Communicate Release**
    - Announce the new release to relevant stakeholders.
    - Update any necessary documentation or user guides.

## Notes

- Ensure all feature branches are merged into `develop` before creating the release branch.
- Conduct regular sync-ups during the release process to address any issues promptly.
- If critical issues are found after merging to `main`, create a hotfix following the hotfix process.
- Consider creating release notes for significant releases, highlighting key features and changes.

## GitHub Actions Workflow

Our GitHub Actions workflow (`ci-cd.yml`) automates several steps in this process, including:
- Running automated tests
- Updating the changelog
- Bumping the version number
- Creating release tags
- Deploying to staging and production

Refer to the `.github/workflows/ci-cd.yml` file for the exact configuration of our CI/CD pipeline.

## Post-Release

- Conduct a retrospective to discuss what went well and what could be improved in the release process.
- Update this document if any process improvements are identified.
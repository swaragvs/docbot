REM filepath: c:\Users\Lenovo\Desktop\things\crackit\init_repo.bat
@echo off
REM Initialize git repo, create initial commit, and optionally add a remote and push.
REM Usage:
REM   init_repo.bat                -> init repo and make initial commit
REM   init_repo.bat https://...git -> init repo, commit, add remote origin and push

setlocal

:: Optional remote URL is first argument
set "REMOTE=%~1"

:: Check for git
where git >nul 2>&1
if errorlevel 1 (
  echo Git not found. Please install Git: https://git-scm.com/ and rerun this script.
  exit /b 1
)

if exist .git (
  echo Repository already initialized in this folder.
  if not "%REMOTE%"=="" (
    echo Adding/updating remote origin and pushing...
    git remote remove origin >nul 2>&1
    git remote add origin "%REMOTE%"
    git branch -M main 2>nul
    git push -u origin main
    if errorlevel 1 (
      echo Failed to push to remote. Check network/auth and the remote URL.
      exit /b 1
    )
    echo Remote set and pushed successfully.
    exit /b 0
  )
  exit /b 0
)

:: Initialize and commit
git init
git add .
git commit -m "Initial commit"

if errorlevel 1 (
  echo Failed to create initial commit. Review 'git status'.
  exit /b 1
)

:: Ensure default branch is 'main'
git branch -M main 2>nul

if not "%REMOTE%"=="" (
  echo Adding remote origin and pushing to %REMOTE% ...
  git remote add origin "%REMOTE%"
  git push -u origin main
  if errorlevel 1 (
    echo Failed to push to remote. Check network/auth and the remote URL.
    exit /b 1
  )
  echo Repository initialized, committed and pushed to remote.
) else (
  echo Repository initialized and initial commit created locally.
)

endlocal
exit /b 0
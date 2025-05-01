# Check if a commit message was provided
param (
    [string]$commitMessage
)

if (-not $commitMessage) {
    Write-Host "Error: No commit message provided."
    Write-Host "Usage: .\git_commit_push.ps1 -commitMessage 'your commit message'"
    exit 1
}

# Add all changes to the staging area
git add .

# Commit with the provided message
git commit -m $commitMessage

# Push the changes to the remote repository
git push
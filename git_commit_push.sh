#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Error: No commit message provided."
  echo "Usage: ./git_commit_push.sh 'your commit message'"
  exit 1
fi

# Add all changes to the staging area
git add .

# Commit with the provided message
git commit -m "$1"

# Push the changes to the remote repository
git push
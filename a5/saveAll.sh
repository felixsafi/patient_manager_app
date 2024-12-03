#!/bin/bash

# Stage all changes
git add .

# Prompt for a commit message
echo "Enter a commit message:"
read COMMIT_MESSAGE

# Commit the changes
git commit -m "$COMMIT_MESSAGE"

# Get the current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Check if we are on a valid branch
if [ -z "$CURRENT_BRANCH" ]; then
  echo "You are not currently on a branch. Please switch to a branch first."
  exit 1
fi

# Push the current branch to origin
git push origin "$CURRENT_BRANCH"

# Pull the latest changes from master
git checkout master
git pull origin master

# Merge the current branch into master
git merge "$CURRENT_BRANCH"

# Push the updated master branch to origin
git push origin master

# Switch back to the current branch
git checkout "$CURRENT_BRANCH"

# Check if the 'd' flag was passed to delete the branch
if [ "$1" == "d" ]; then
  git checkout master
  git branch -d "$CURRENT_BRANCH"
  git push origin --delete "$CURRENT_BRANCH"
fi

echo "Changes from $CURRENT_BRANCH have been merged into master and pushed to origin."

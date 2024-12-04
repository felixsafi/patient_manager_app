#!/bin/bash

# Function to check if a branch name is valid
is_valid_branch() {
  # Check if the branch name exists in the list of all branches
  git branch -a | grep -q "remotes/origin/$1\|$1"
}

# Prompt the user to enter a branch name until a valid one is provided
BRANCH=""
while true; do
  echo "Enter the branch you want to work on:"
  read BRANCH
  if is_valid_branch "$BRANCH"; then
    break  # Valid branch name, exit the loop
  else
    echo "Invalid branch name. Please try again."
  fi
done

# Pull the latest changes from the origin master branch updated device master
echo "Getting Updates..."
git checkout master
git pull origin master

# Switch to the desired branch
echo "Switching to $BRANCH branch..."
git checkout $BRANCH

echo "Merging the latest changes from master into $BRANCH..."
git merge master

echo "Update complete, $BRANCH. updated"
echo "run ./saveAll after to update things"
echo "run ./testAll to run all tests"
echo "run ./test <testName> to run a specific test"


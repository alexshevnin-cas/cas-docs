#!/bin/bash
# Import all existing GitHub Issues to Asana
#
# Usage:
#   export ASANA_TOKEN="your-personal-access-token"
#   export ASANA_PROJECT_GID="your-project-gid"
#   bash .github/scripts/import-issues-to-asana.sh
#
# Prerequisites:
#   - gh CLI authenticated
#   - curl, jq installed

set -euo pipefail

if [ -z "${ASANA_TOKEN:-}" ] || [ -z "${ASANA_PROJECT_GID:-}" ]; then
  echo "Error: Set ASANA_TOKEN and ASANA_PROJECT_GID environment variables"
  echo ""
  echo "  export ASANA_TOKEN='1/12345...'        # Asana Personal Access Token"
  echo "  export ASANA_PROJECT_GID='123456789'    # Asana Project GID"
  exit 1
fi

API="https://app.asana.com/api/1.0"

# Get workspace GID from project
WORKSPACE_GID=$(curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "$API/projects/$ASANA_PROJECT_GID?opt_fields=workspace" | jq -r '.data.workspace.gid')

echo "Workspace: $WORKSPACE_GID"
echo "Project: $ASANA_PROJECT_GID"

# Get sections (for mapping labels to sections)
echo ""
echo "Fetching sections..."
SECTIONS=$(curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "$API/projects/$ASANA_PROJECT_GID/sections" | jq -r '.data')

# Create sections if they don't exist
for TRACK in Core Data Portal Services Finance Growth DX BX; do
  SECTION_GID=$(echo "$SECTIONS" | jq -r ".[] | select(.name == \"$TRACK\") | .gid")
  if [ -z "$SECTION_GID" ] || [ "$SECTION_GID" = "null" ]; then
    echo "Creating section: $TRACK"
    SECTION_GID=$(curl -s -X POST -H "Authorization: Bearer $ASANA_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"data\": {\"name\": \"$TRACK\"}}" \
      "$API/projects/$ASANA_PROJECT_GID/sections" | jq -r '.data.gid')
  fi
  echo "  $TRACK → $SECTION_GID"
  eval "SECTION_${TRACK}=$SECTION_GID"
done

# Fetch all open issues from GitHub
echo ""
echo "Fetching GitHub issues..."
ISSUES=$(gh issue list --limit 100 --state open --json number,title,body,labels,url)
COUNT=$(echo "$ISSUES" | jq length)
echo "Found $COUNT issues"

echo ""
echo "Importing..."

echo "$ISSUES" | jq -c '.[]' | while read -r ISSUE; do
  NUMBER=$(echo "$ISSUE" | jq -r '.number')
  TITLE=$(echo "$ISSUE" | jq -r '.title')
  BODY=$(echo "$ISSUE" | jq -r '.body // ""')
  URL=$(echo "$ISSUE" | jq -r '.url')
  LABELS=$(echo "$ISSUE" | jq -r '[.labels[].name] | join(", ")')

  # Find track label
  TRACK=$(echo "$ISSUE" | jq -r '[.labels[].name] | map(select(. == "Core" or . == "Data" or . == "Portal" or . == "Services" or . == "Finance" or . == "Growth" or . == "DX" or . == "BX")) | first // empty')

  # Build notes
  NOTES=$(printf "%s\n\n---\nGitHub: %s\nLabels: %s" "$BODY" "$URL" "$LABELS")

  # Create task
  TASK_GID=$(curl -s -X POST -H "Authorization: Bearer $ASANA_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg name "$TITLE #$NUMBER" --arg notes "$NOTES" --arg project "$ASANA_PROJECT_GID" \
      '{data: {name: $name, notes: $notes, projects: [$project]}}')" \
    "$API/tasks" | jq -r '.data.gid')

  # Move to section
  if [ -n "$TRACK" ] && [ "$TRACK" != "null" ]; then
    SECTION_VAR="SECTION_${TRACK}"
    SECTION_GID="${!SECTION_VAR:-}"
    if [ -n "$SECTION_GID" ]; then
      curl -s -X POST -H "Authorization: Bearer $ASANA_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"data\": {\"task\": \"$TASK_GID\"}}" \
        "$API/sections/$SECTION_GID/addTask" > /dev/null
    fi
  fi

  echo "  #$NUMBER → $TASK_GID [$TRACK] $TITLE"
done

echo ""
echo "Done! Check your Asana project."

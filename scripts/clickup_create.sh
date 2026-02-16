#!/bin/bash
# Create a task in ClickUp
# Usage: bash scripts/clickup_create.sh "Task name" "Description" [assignee]
#
# Assignee: ruslan | alexei | borys (or ClickUp user ID)
#
# Examples:
#   bash scripts/clickup_create.sh "b2b.cas.ai Fix login bug" "Auth token expires too early" ruslan
#   bash scripts/clickup_create.sh "b2b.cas.ai Update docs" "Refresh metrics dictionary"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env.clickup"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found"
  echo "Create it with: CLICKUP_API_TOKEN, CLICKUP_LIST_ID"
  exit 1
fi

source "$ENV_FILE"

if [ -z "$1" ]; then
  echo "Usage: $0 \"Task name\" \"Description\" [assignee]"
  echo "Assignee: ruslan | alexei | borys | <user_id>"
  exit 1
fi

NAME="$1"
DESC="${2:-}"
ASSIGNEE_INPUT="${3:-}"

# Resolve assignee name to ID
ASSIGNEE_ID=""
case "$ASSIGNEE_INPUT" in
  ruslan)  ASSIGNEE_ID="$CLICKUP_RUSLAN_ID" ;;
  alexei)  ASSIGNEE_ID="$CLICKUP_ALEXEI_ID" ;;
  borys)   ASSIGNEE_ID="$CLICKUP_BORYS_ID" ;;
  "")      ASSIGNEE_ID="" ;;
  *)       ASSIGNEE_ID="$ASSIGNEE_INPUT" ;;
esac

ASSIGNEES_JSON="[]"
if [ -n "$ASSIGNEE_ID" ]; then
  ASSIGNEES_JSON="[$ASSIGNEE_ID]"
fi

PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
    'name': sys.argv[1],
    'markdown_description': sys.argv[2],
    'tags': ['bi-mvp'],
    'assignees': $ASSIGNEES_JSON
}))
" "$NAME" "$DESC")

RESULT=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$CLICKUP_LIST_ID/task" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'err' in d:
    print(f'Error: {d[\"err\"]}')
else:
    print(f'Created: {d[\"name\"]}')
    print(f'URL:     {d[\"url\"]}')
" 2>/dev/null

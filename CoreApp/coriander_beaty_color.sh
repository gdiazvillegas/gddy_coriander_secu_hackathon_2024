#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Function to set color based on severity level
get_severity_color() {
    case $1 in
        "Low") echo -n "$YELLOW" ;;
        "Medium") echo -n "$BLUE" ;;
        "High") echo -n "$PURPLE" ;;
        "Critical") echo -n "$RED" ;;
        *) echo -n "$RESET" ;;
    esac
}

# Read JSON from file
json_file="$1"
if [ ! -f "$json_file" ]; then
    echo "Error: File not found!"
    exit 1
fi

# Parse JSON and format output
coriander_status=$(jq -r '.coriander_status' "$json_file")
findings=$(jq -c '.findings[]' "$json_file")

# Print Coriander status
if [ "$coriander_status" == "failed" ]; then
    echo -e "${BOLD}Coriander Status:${RESET} ${RED}$coriander_status${RESET}"
else
    echo -e "${BOLD}Coriander Status:${RESET} ${GREEN}$coriander_status${RESET}"
fi

echo -e "\n${BOLD}Security Findings:${RESET}\n"

print_field() {
    local label=$1
    local value=$2
    local color=${3:-$RESET}
    printf "${BOLD}%-20s${RESET} ${color}%-80s${RESET}\n" "$label:" "$value"
}

echo "$findings" | while read -r finding; do
    title=$(echo "$finding" | jq -r '.title')
    description=$(echo "$finding" | jq -r '.description')
    location=$(echo "$finding" | jq -r '.location')
    impact=$(echo "$finding" | jq -r '.impact')
    recommendation=$(echo "$finding" | jq -r '.recommendation')
    severity_level=$(echo "$finding" | jq -r '.severity_level')
    severity_color=$(get_severity_color "$severity_level")

    echo -e "${BOLD}${CYAN}$title${RESET}"
    print_field "Description" "$description"
    print_field "Location" "$location"
    print_field "Impact" "$impact"
    print_field "Recommendation" "$recommendation"
    print_field "Severity Level" "$severity_level" "$severity_color"
    echo
done

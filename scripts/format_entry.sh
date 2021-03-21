#!/bin/bash

read -p "Does the project have a homepage (different from where the source code is hosted)? [y/N] " has_homepage
[[ "$has_homepage" == [Yy]* ]] && has_homepage=true || has_homepage=false
$has_homepage && echo "You entered 'Yes'" || echo "You entered 'No'"

read -p "Project name: " name

$has_homepage && message="Homepage URL: " || message="Source code URL: "
read -p "$message" main_url

read -p "Description (avoid redundancy, keep it short, end with '.'): " description
$has_homepage && read -p "Source code URL: " source_code_url
read -p "License: " license

echo ""
echo "Copy this entry to your clipboard, paste it in the appropriate place in the README.md:"
if $has_homepage; then
    echo "- [$name]($main_url) - $description ([Source Code]($source_code_url)) \`$license\`"
else
    echo "- [$name]($main_url) - $description \`$license\`"
fi

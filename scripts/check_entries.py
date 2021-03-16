# This script checks the format of the entries in the list.

import re, sys

_anything_regex = r"(.+)"
format_1_regex = re.compile(
    r"^- \[%s\]\(%s\) - %s\. \(\[Source Code\]\(%s\)\) `%s`$" % ((_anything_regex,) * 5)
)
format_2_regex = re.compile(r"^- \[%s\]\(%s\) - %s\. `%s`$" % ((_anything_regex,) * 4))

lines = []

with open("README.md") as f:
    # Stupid logic to only process the rows about the list
    hr_counter = 0
    for i, line in enumerate(f):
        if line == "---\n":
            hr_counter += 1

            if hr_counter > 2:
                break

            continue

        if hr_counter < 2:
            continue

        if line.startswith("-"):
            lines.append((i + 1, line[:-1]))

errors = []
for line_number, line in lines:
    m = format_1_regex.match(line)
    if m:
        name, homepage, description, code_url, license = m.groups()
        continue

    m = format_2_regex.match(line)
    if m:
        name, code_url, description, license = m.groups()
        continue

    errors.append("Line %s is not formatted correctly:\n %s\n" % (line_number, line))

if errors:
    for e in errors:
        print(e)
    sys.exit(1)

print("All entries seem to be correctly formatted.")

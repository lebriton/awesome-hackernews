import re, sys
from collections import defaultdict


_anything_regex = r"(.+)"
format_1_regex = re.compile(
    r"^- \[%s\]\(%s\) - %s\. \(\[Source Code\]\(%s\)\) `%s`$" % ((_anything_regex,) * 5)
)
format_2_regex = re.compile(r"^- \[%s\]\(%s\) - %s\. `%s`$" % ((_anything_regex,) * 4))


def parse_readme():
    data = defaultdict(list)
    with open("README.md") as f:
        # The list is between the 2nd and 3rd horizontal rules (hr).
        hr_counter = 0

        for line_number, line in enumerate(f, start=1):
            line = line[:-1]

            if line == "---":
                hr_counter += 1
                if hr_counter > 2:
                    break
                continue
            if hr_counter < 2:
                continue

            if line.startswith("#"):
                current_section = (line_number, line.lstrip("#")[1:])
            elif line.startswith("-"):
                data[current_section].append((line_number, line))
    return dict(data)


def lint_entry(entry):
    line_number, line = entry

    # BBB: walrus operator
    m = format_1_regex.match(line) or format_2_regex.match(line)
    if m:
        name = m.group(1)
        if hasattr(lint_entry, "previous_name"):
            if name.lower() < lint_entry.previous_name.lower():
                yield "l%s: entry is not inserted correctly in case-insensitive alphabetical order (compared to l%s)" % (
                    line_number,
                    line_number - 1,
                )
        # XXX: using this is a bit hacky
        lint_entry.previous_name = name
    else:
        yield "l%s: entry is not formatted correctly" % line_number


def lint():
    errors = []

    for section_name, sublist in parse_readme().items():
        for entry in sublist:
            errors.extend(lint_entry(entry))
        del lint_entry.previous_name

    if errors:
        for e in errors:
            print(e)
        print("\n%s errors" % len(errors))
        sys.exit(1)
    print("0 error")


if __name__ == "__main__":
    lint()

#!/usr/bin/sh

examples=$(ls -d examples/*/. | sed "s|/\.||g" | paste -s -d' ')
for example_dir in $examples;do
  cat << EOM > "$example_dir/README.md"
# \`$(echo "$example_dir" | cut -d/ -f2)\`

$(cat "$example_dir/description.txt")

File layout:
\`\`\`
~ tree "$example_dir/root"
$(tree "$example_dir/root")
\`\`\`

Command:
\`\`\`
$(cat "$example_dir/command.sh")
\`\`\`

Result:
\`\`\`json
$(jq '.' "$example_dir/result.json")
\`\`\`

$([ -f "$example_dir/epilog.txt" ] && cat "$example_dir/epilog.txt")
EOM
done

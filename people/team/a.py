import re
from pathlib import Path

md_dir = Path(".")
img_base = ".img"

for md_file in md_dir.glob("*.md"):
    if md_file.name == "README.md":
        continue

    content = md_file.read_text(encoding="utf-8")

    # If already has column block, update width if needed
    if "{% columns %}" in content:
        updated = content.replace('{% column width="66.66666666666666%" %}', '{% column width="70%" %}')
        if updated != content:
            md_file.write_text(updated, encoding="utf-8")
            print(f"🔁 Updated width in {md_file.name}")
        else:
            print(f"⏭ Already up-to-date: {md_file.name}")
        continue

    split_marker = "#### Core work interests related to Solving FCB"
    if split_marker not in content:
        print(f"⏭ Skipping {md_file.name} — no marker")
        continue

    top, bottom = content.split(split_marker, 1)

    def extract_block(label):
        match = re.search(fr"#### {label}\n+(.*?)(?=\n####|\Z)", top, re.DOTALL)
        return match.group(1).strip() if match else ""

    institution = extract_block("Institution")
    email = extract_block("Email")
    affiliations = extract_block("Affiliations")

    name = md_file.stem
    img_url = f"https://raw.githubusercontent.com/Solving-FCB/docs/refs/heads/main/{img_base}/{name}.webp"

    left = ""
    if institution:
        left += f"#### Institution\n\n{institution}\n\n"
    if email:
        left += f"#### Email\n\n{email}\n\n"
    if affiliations:
        left += f"#### Affiliations\n\n{affiliations}\n"

    columns_block = f"""{{% columns %}}
{{% column width="70%" %}}
{left.strip()}
{{% endcolumn %}}

{{% column %}}
<figure><img src="{img_url}" alt=""></figure>
{{% endcolumn %}}
{{% endcolumns %}}

"""

    header = top.strip().splitlines()[0]
    new_content = f"{header}\n\n{columns_block}#### Core work interests related to Solving FCB{bottom}"

    md_file.write_text(new_content, encoding="utf-8")
    print(f"✅ Inserted columns in {md_file.name}")

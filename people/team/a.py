import re
from pathlib import Path

md_dir = Path(".")
img_base = ".img"

for md_file in md_dir.glob("*.md"):
    if md_file.name == "README.md":
        continue

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    if "{% columns %}" in content:
        continue  # skip if already processed

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

    name = md_file.stem  # e.g. aheto-d
    img_url = f"https://raw.githubusercontent.com/Solving-FCB/docs/refs/heads/main/{img_base}/{name}.webp"

    left = ""
    if institution:
        left += f"#### Institution\n\n{institution}\n\n"
    if email:
        left += f"#### Email\n\n{email}\n\n"
    if affiliations:
        left += f"#### Affiliations\n\n{affiliations}\n"

    columns_block = f"""{{% columns %}}
{{% column width="66.66666666666666%" %}}
{left.strip()}
{{% endcolumn %}}

{{% column %}}
<figure><img src="{img_url}" alt=""></figure>
{{% endcolumn %}}
{{% endcolumns %}}

"""

    new_content = f"{top.strip().splitlines()[0]}\n\n{columns_block}#### Core work interests related to Solving FCB{bottom}"

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Processed {md_file.name}")

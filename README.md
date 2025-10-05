This script helps with migrating notes from Dropbox Paper.
Specifically, it makes Paper->Notion migration, and Paper->Obsidian migration less painful.

![Comparison](/demo/side-by-side-comparison.png?raw=true "Comparison")
On the left is a Dropbox Paper note imported directly into Notion. On the right, the Paper note is converted before being imported into Notion.

### Installation
Install Python 3.

## Use case: Dropbox Paper -> Notion

### Problem
If you export a Dropbox Paper document as a .md file, and import it into Notion.
The formatting will be off:
1. Blank lines between paragraphs are not preserved.
2. Indented checklists are often not recognized as checklists.
3. Sometimes quotes will not be imported as quotes.
4. ... and more.

You will then have to painstakingly fix it manually.

### Solution
I wrote this script to fix the first three issues listed above, so that I can spend less time fixing it manually. 
This script does not fix all the issues, and you will still need to manually fix some remaining issues.


### Usage
1. Export a Dropbox Paper document as .md file. Let's say it's named `Paper_Note.md`.
If you directly import it into Notion, the formatting will be quite off, as mentioned in the Overview section above.

2. Run the script:
```
python3 convert.py --line-break-trick <input file> <output save folder>
```
In this case:
```
python3 convert.py --line-break-trick ~/Downloads/Paper_Note.md ~/Downloads/
```

3. The converted output file will have the same name as the input file, except that underscores will be replaced with spaces. So in this case, `~/Downloads/Paper Note.md` is generated.
4. Import the converted file into Notion. You will notice that there are a lot of weird characters of `␣` in the imported Notion note. This is a side effect of the script's attempt to preserve blank lines between paragraphs. In Notion, hit `Ctrl+F`, search for `␣`, and replace all with either a space or nothing.
5. Compare with the original note and manually fix some remaining issues not handled by this script.

### Failure Cases
- If a quote is followed by a deeper indented bullet point in a Dropbox Paper document, Notion does not support that.
  - The bullet point will be imported by Notion as a (plain text) code block.
  - It's not just Notion can't import it properly. It's that this is just not allowed on Notion's editor at all.
  - The only workaround I found is to also quote the deeply indented point. But that looks weird to me, and it's a hassle to implement that. So I just don't handle this case.


## Use case: Dropbox Paper -> Obsidian
```
python3 convert.py <input file> <output save folder>
```


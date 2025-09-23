

### Usage
```
convert.py <input file> <output save folder>
```

### Failure Cases
- If a quote is followed by a deeper indented bullet point, Notion does not support that.
 - The bullet point will be imported by Notion as a (plain text) code block.
 - It's not just Notion can't import it properly. It's that it's not possible to achieve on Notion's editor as well.
 - The only workaround I found is to also quote the deeply indented point. But that looks weird to me, and it's a hassle to implement that.


### Usage
```
convert.py <input file> <output save folder>
```

### Failure Cases
- If a quote is followed by a deeper indented bullet point, Notion does not support that.
 - It's not just Notion can't import it properly. It's that it's not possible to achieve on Notion's editor as well.
 - The bullet point will be imported as a (plain text) code block.
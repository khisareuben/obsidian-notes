
# Comprehensive Notes on Using Markdown in Obsidian

Obsidian uses Markdown as its core formatting language. Markdown is a lightweight markup language that allows you to format text using plain text syntax. Below is a complete guide to all the features you can use in Obsidian.

---

## 1. Headings

- `# Heading 1`
    
- `## Heading 2`
    
- `### Heading 3`
    
- `#### Heading 4`
    
- `##### Heading 5`
    
- `###### Heading 6`
    

---

## 2. Emphasis

- _Italic_: `*text*` or `_text_`
    
- **Bold**: `**text**` or `__text__`
    
- _**Bold and Italic**_: `***text***`
    
- ~~Strikethrough~~: `~~text~~`
    

---

## 3. Lists

### Unordered Lists

```
- Item 1
- Item 2
  - Subitem
```

### Ordered Lists

```
1. First item
2. Second item
   3. Subitem
```

### Task Lists

- [ ] 
    
    Incomplete task
    
- [ ] 
    
    Completed task
    

```

---

## 4. Links
- Inline link: `[text](URL)`
- Internal link: `[[Note Name]]`
- Aliased link: `[[Note Name|Alias]]`

---

## 5. Images
```

![Alt text](image_url)

```

For local images, place them in your vault and reference them with relative paths.

---

## 6. Blockquotes
```

> This is a blockquote.
> 
> > Nested blockquote.

```

---

## 7. Code
### Inline Code
```

`inline code`

```

### Code Blocks
```

```
Code here
```

````

---

## 8. Horizontal Rule
```
---
```

---

## 9. Tables
```
````

| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |

```

---

## 10. Footnotes
```

Here is a footnote reference[^1].

[^1]: This is the footnote.

```

---

## 11. Callouts (Obsidian-specific)
```

> [!note] This is a note callout.

> [!warning] This is a warning callout.

```

Types include: `note`, `info`, `tip`, `important`, `warning`, `caution`, `example`, `quote`.

---

## 12. Embeds
- Embed another note: `![[Note Name]]`
- Embed a specific section: `![[Note Name#Section]]`
- Embed an image or file: `![[image.png]]`

---

## 13. Tags
- Add tags with `#tag`
- Nested tags: `#tag/subtag`

---

## 14. Math (LaTeX)
- Inline math: `$x^2 + y^2 = z^2$`
- Block math:
```

$$ \frac{a}{b} = c $$

```

---

## 15. Comments
Obsidian supports comments using HTML syntax:
```

<!-- This is a comment -->

```

---

## 16. Advanced Obsidian Features
- **Links to headings**: `[[Note#Heading]]`
- **Links to blocks**: `[[Note^blockID]]`
- **Aliases**: Defined in frontmatter YAML.
- **Frontmatter YAML**: Add metadata at the top of a note:
```

---

## title: My Note tags: [tag1, tag2]

```

---

## 17. Plugins Enhancing Markdown
- **Dataview**: Query notes with SQL-like syntax.
- **Templater**: Automate repetitive content.
- **Advanced Tables**: Better table formatting.
- **Kanban**: Create boards using Markdown lists.

---

## 18. Best Practices
- Use consistent heading levels.
- Organize notes with tags and links.
- Use callouts for emphasis.
- Keep metadata in frontmatter for easy searching.
- Leverage plugins for advanced workflows.

---

## 19. Quick Reference Cheat Sheet
```

|Feature|Syntax Example|
|---|---|
|Bold|`**text**`|
|Italic|`*text*`|
|Link|`[text](url)`|
|Image|`![alt](url)`|
|Task List|`- [ ] task`|
|Table|`|a|b|`|
|Footnote|`[^1]`|
|Callout|`> [!note]`|
|Math|`$x+y=z$`|

---

# Conclusion

With Markdown in Obsidian, you can create richly formatted notes, link ideas together, embed files, and extend functionality with plugins. Mastering these features will unlock the full potential of Obsidian as a powerful knowledge management tool.
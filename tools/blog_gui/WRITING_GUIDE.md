# Writing Guide

The editor shows formatted content while keeping the saved file as Markdown.

## Mathematics

For a post containing equations, open **Properties** and enable **Math**. This adds the MathJax include required by the published Jekyll page.

### Live display-math editing

1. Move to an empty line.
2. Type `$$` and then press **Space**.
3. The paragraph becomes a LaTeX block with a rendered preview.
4. Type only the equation body, without opening or closing `$$` delimiters.

The preview updates while you type. You can also type `/` on an empty line and choose **Math** to create the same block.

### Inline math

For a short expression inside a sentence, type the complete expression with one dollar sign on each side. It becomes a rendered inline formula after the closing `$` is entered:

```markdown
The treatment effect is $\tau = E[Y(1) - Y(0)]$.
```

### Display math

The saved Markdown representation uses two dollar signs around a separate equation block:

```markdown
$$
\hat{\tau}
= \frac{1}{n_1}\sum_{i:D_i=1}Y_i
- \frac{1}{n_0}\sum_{i:D_i=0}Y_i
$$
```

<!-- RENDERED_MATH_EXAMPLE -->

Do not pre-type both `$$` lines and then place the cursor between them when editing visually. Use `$$` followed by **Space**, or `/` followed by **Math**, so the editor can create a live LaTeX block first.

### Common LaTeX

| Result | Write |
|---|---|
| Fraction | `\frac{a}{b}` |
| Square root | `\sqrt{x}` |
| Superscript | `x^2` |
| Subscript | `x_i` |
| Sum | `\sum_{i=1}^{n}` |
| Integral | `\int_0^1` |
| Greek letter | `\alpha`, `\beta`, `\tau` |
| Hat | `\hat{\theta}` |
| Bold symbol | `\mathbf{x}` |

## Basic Markdown

Start a line with the marker, then press Space. The editor converts it into a formatted block.

| Purpose | Markdown |
|---|---|
| Heading 1 | `# Heading` |
| Heading 2 | `## Heading` |
| Heading 3 | `### Heading` |
| Bold | `**bold**` |
| Italic | `*italic*` |
| Strikethrough | `~~removed~~` |
| Inline code | `` `code` `` |
| Bullet list | `- item` |
| Numbered list | `1. item` |
| Task | `- [ ] todo` or `- [x] done` |
| Quote | `> quoted text` |
| Link | `[label](https://example.com)` |
| Divider | `---` |

### Code block

Use three backticks and optionally add a language:

~~~markdown
```python
def hello():
    print("Hello")
```
~~~

### Table

```markdown
| Variable | Meaning |
|---|---|
| Y | Outcome |
| D | Treatment |
```

## Keyboard Shortcuts

These shortcuts are for macOS.

| Action | Shortcut |
|---|---|
| Bold selected text | `⌘ B` |
| Italic selected text | `⌘ I` |
| Undo | `⌘ Z` |
| Redo | `⌘ ⇧ Z` |
| Line break without a new paragraph | `Shift Enter` |
| Open the block menu | Type `/` on an empty line |

## Editing Tips

- Select text to open the floating formatting toolbar.
- Type `/` on an empty line to insert headings, lists, tasks, tables, code, or math.
- Press Enter twice to leave a list or quote block.
- Use a blank line between paragraphs in the saved Markdown.
- Click **Save Draft** or **Save Published Post** before switching documents.
- Image upload is intentionally disabled; blog images should be added as repository assets.

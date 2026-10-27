# Writing the blog

Open this folder in VS Code. Quarto and its VS Code extension are already installed
on the inspected machine. The new-post helper uses Python 3.9+ and no extra packages.

## New Post → Write → Preview → Publish

1. Run **Tasks: Run Task → Blog: New Post** from the command palette
   (`Cmd+Shift+P`). Enter a title and optional comma-separated categories.
   The task opens `posts/YYYY-MM-DD-title-slug/index.qmd` in VS Code.
   The date uses Asia/Jerusalem. Existing folders are never overwritten.
2. Write in the source editor or use **Quarto: Edit in Visual Mode**.
3. Use Quarto's Preview button for the current post, or the **Blog: Preview**
   task for the site. Drafts are visible in preview. Stop the site preview with
   `Ctrl+C` in its terminal before the final render.
4. Check the publication date; changing the date in YAML does not require
   renaming the directory. New posts are included in the next render by default.
5. Run **Blog: Render for publishing**. Check that rendering succeeds, inspect
   the changed files in Source Control, then commit the source, images, and
   regenerated `docs/` files and push using VS Code's Source Control.
   A preview is not a substitute for this final full render: previews show drafts.

Terminal alternative:

```sh
python3 scripts/new_post.py "My New Post" --categories "math, physics" --open
quarto preview
# Once ready, stop preview, then:
quarto render
```

Run the script without arguments for terminal prompts. Use `--slug my-url-slug`
for an explicit slug (including titles that cannot be transliterated to ASCII),
or `--date 2026-10-27` for an explicit date. Do not rename published folders:
their names form the post URLs.

## Metadata

New posts contain only:

```yaml
---
title: "My New Post"
date: 2026-10-27
categories: [math]
---
```

`posts/_metadata.yml` already supplies `author: Yair Mau`, `toc: false`,
`title-block-banner: false`, and `freeze: auto`. No shared-metadata change is
needed. Post-specific options override these defaults; keep `toc: true` on
articles that benefit from it. `layout: post` is unnecessary for new Quarto
posts. Keep title, fixed publication date, categories, and optional
description/image on each article. Add `draft: true` manually only if you want
to exclude an unfinished post from publishing. Do not put `draft: true` in shared metadata:
that would also hide existing posts. Avoid `date: today`, which changes on render.

## Images

Keep images next to `index.qmd`, optionally in an `images/` subfolder. In Quarto's
visual editor, use **Insert → Figure** to select an image and copy it into the
post folder when prompted. Clipboard image handling depends on the editor and
clipboard format; it has not been interactively tested here. The reliable source
mode fallback is to drag/copy the file into the post folder in Explorer and use:

```markdown
![A useful description](images/diagram.png)
```

VS Code's built-in Markdown paste/drop settings are not assumed to apply to the
Quarto language mode. Keep `.qmd` files in Quarto mode for its math and preview tools.

A separate cover is unnecessary. Quarto listings discover an article image
automatically, falling back to the first image. To choose a specific existing
image reliably, add `image: images/diagram.png` to that post's YAML. An optional
`description` supplies the listing excerpt; otherwise Quarto uses article text.

## Publishing setup and limitations

The inspected repository has `output-dir: docs`, tracked rendered HTML/assets,
`docs/.nojekyll`, and no `.github/workflows` or Quarto publish configuration.
Commit history shows source changes committed alongside regenerated `docs/`.
This matches Quarto's render-locally / GitHub Pages deploy-from-branch approach.
The remote Pages settings were not verified: confirm **Settings → Pages →
Deploy from a branch → main → /docs** if publishing needs troubleshooting.
No deployment settings, existing posts, URLs, or theme have been changed.

`_environment` selects `/Users/yairmau/miniforge3/envs/olympus/bin/python`
for Quarto's Python execution. This environment must contain the dependencies
used by the computational posts. `freeze: auto` helps reuse saved
computations, but the repository has frozen results for only two post folders;
it does not guarantee a dependency-free fresh build. Notebook outputs can also
contain results saved in the notebook itself.

GitHub Actions could render and deploy on every push, but first needs a portable
Python configuration and a reproducible dependency/freeze strategy. Keeping
local rendering and the existing hosting mechanism is the smaller initial step.
The render task deliberately does not commit or push automatically.

## Quartize assessment

Quartize is not installed. Its documented palette and form workflows create
Quarto posts, so the standard `posts/<folder>/index.qmd` organization is a plausible
fit. It offers author/category defaults and featured-image fields. Its published
settings document no draft default or custom-template option; exact generated
paths and behavior were not tested. The Python task was chosen for predictable
dated paths and minimal metadata, with no new extension dependency.

If trying the form later, install `coatless.quartize` from Extensions and use
**Quartize: New Blog Post (Open Plugin)**. Workspace settings can supply
`quartize.authors: ["Yair Mau"]`, `quartize.defaultAuthor: "Yair Mau"`, and
`quartize.categories: ["math", "physics", "origami", "projects", "science", "question"]`.
Inspect the generated metadata before publishing.

References: [Quartize](https://marketplace.visualstudio.com/items?itemName=coatless.quartize),
[Quarto blogs](https://quarto.org/docs/websites/website-blog.html),
[drafts](https://quarto.org/docs/websites/website-drafts.html),
[listing images](https://quarto.org/docs/websites/website-listings.html#listing-fields),
[visual editing](https://quarto.org/docs/tools/vscode/visual-editor.html),
[GitHub Pages publishing](https://quarto.org/docs/publishing/github-pages.html).

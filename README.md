# Chendi Qian’s personal website

[Jekyll](https://jekyllrb.com/) website based on [al-folio](https://github.com/alshedivat/al-folio), published at **https://chendiqian.github.io**.

## Where to make changes

| Content | File |
| --- | --- |
| Biography, subtitle, research tagline, portrait settings | `_pages/about.md` |
| Homepage highlights (newest first; Markdown supported) | `_data/highlights.yml` |
| Publications and selected papers | `_bibliography/papers.bib` |
| CV, education, awards | `assets/json/resume.json` |
| Email, social profiles, site description | `_config.yml` |
| Custom colors, typography, spacing, mobile layout | `_sass/_personal.scss` |
| Profile photo | `assets/img/prof_pic.jpg` |
| Publication thumbnails | `assets/img/publication_preview/` |

The CV reads **`assets/json/resume.json`**. `_data/cv.yml` is an unused theme fallback, not your active CV. `_site/` is generated output: never edit it directly.

### Add a paper

Copy an entry in `_bibliography/papers.bib`, give it a unique citation key, and update the title, authors, year, venue, and links. Add `selected={true}` to feature it on the homepage. The `preview` filename must exist in `assets/img/publication_preview/`. To announce an acceptance, also add an entry to `_data/highlights.yml`.

### Add an award

Insert an object at the top of the `awards` array in `assets/json/resume.json`, using the existing `title`, `date` (`YYYY-MM`), `awarder`, and `summary` fields. Keep valid JSON, including commas between entries. Add a separate short announcement to `_data/highlights.yml` if it should appear on the homepage too.

## Preview locally

You need Ruby, Bundler, and Python 3. GitHub’s build uses Ruby **3.2.2** (see `.github/workflows/deploy.yml`); the current site also builds locally with Ruby 3.3.5.

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open http://127.0.0.1:4000. Content edits rebuild automatically; restart the server after editing `_config.yml`. Stop with Ctrl+C. The inherited demo posts may need additional tools for notebook or diagram rendering; these are not required for the homepage, publications, or CV.

## Check before publishing

```sh
bash bin/check-site
```

This builds the site and checks the homepage, publications, and CV for missing internal link destinations, missing local image/script/style files, broken local fragment links, and duplicate HTML IDs. It also parses the CV JSON. External URLs are not checked. CI runs the same generated-page checks before deploying.

## Publish

Commit the intended files and push to `master`. The [deploy workflow](https://github.com/chendiqian/chendiqian.github.io/actions/workflows/deploy.yml) builds the site and publishes `_site/` to `gh-pages`; GitHub Pages then updates the public website. Pull requests build and check without publishing. Do not edit or manually push generated files to `gh-pages`, or use the inherited `bin/deploy` helper for routine updates.

If publishing fails, inspect the failed step in GitHub Actions. The existing site remains available until deployment succeeds. To undo a published change, revert its source commit and push the revert to `master`.

## Theme maintenance

Personal styles live in `_sass/_personal.scss`; homepage highlights have their own `_includes/highlights.html` partial. Keep new content in data/Markdown files where possible. The original theme manual is preserved in [docs/al-folio.md](docs/al-folio.md); some of its relative links assume the upstream repository layout.

This repository still contains inherited demo pages, posts, and theme tools. They are retained to avoid silently removing existing URLs. Dependency versions and demo cleanup can be reviewed separately; `Gemfile.lock` is currently ignored, so fresh installs can resolve newer dependencies.

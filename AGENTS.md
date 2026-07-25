# Agent instructions for the Lesson Llama project

## Blog publishing workflow

The Lesson Llama blog is now part of the Astro site. Posts live as Markdown files in `src/content/blog/`. The site is built statically and deployed to Cloudflare.

### How to publish a new post

1. Research and draft the article.
2. Create a Markdown file at:

   ```text
   src/content/blog/<slug>.md
   ```

   Use a URL-safe slug (kebab-case, lowercase, no dates). Example: `ai-and-ib-lesson-planning.md`.

3. Start the file with this frontmatter:

   ```yaml
   ---
   title: "Post title in sentence case"
   description: "One or two sentences summarising the post. Used for cards and meta tags."
   pubDate: 2026-07-24
   tags: ["IB MYP", "AI in Education", "Lesson Planning"]
   author: "Lucy"          # optional — defaults to Lucy
   # subtitle: "Optional longer subheadline"  # optional
   # cover: "/blog-covers/<slug>.png"          # optional
   ---
   ```

   - `description`: keep it under 160 characters.
   - `pubDate`: use today's date in `YYYY-MM-DD`.
   - `tags`: 2–4 relevant tags. Prefer tags like "IB MYP", "IGCSE", "A-Level", "AP", "AI in Education", "Lesson Planning", "International Schools", "Product Updates".
   - `author`: optional. Defaults to `Lucy` if omitted.
   - `subtitle`: optional. Appears below the title on the post page.
   - `cover`: optional. Path to an image in `public/`. Example: `/blog-covers/my-post.png` (place the actual image at `public/blog-covers/my-post.png`).
   - `draft: true` can be used for work-in-progress posts that should not be published.

4. Write the body in Markdown. Use `##` for section headings. Keep paragraphs concise. Use international English spelling (the audience is international school teachers). Do not add a sign-off CTA about the waitlist — the page template already appends one.

5. Commit and push. Publishing mode:

   - **Autonomous mode:** commit directly to `main` and push.
   - **Reviewed mode (recommended):** create a branch `post/<slug>`, push it, and open a pull request. Notify the human via Telegram with the PR URL.

6. Deployment:
   - If Cloudflare is connected to this repo (Pages/Workers git integration), pushing/merging to `main` triggers a deploy automatically.
   - If not, a human must run `npm run build && npx wrangler deploy` from this directory after the push.

### Style guidelines

- Audience: international school teachers (IB MYP, IGCSE, A-Level, AP, Australian/Canadian curricula).
- Tone: practical, friendly, and direct. Write as Lucy the Llama — helpful, not salesy.
- Length: roughly 800–1,200 words.
- Avoid overpromising features. Lesson Llama is pre-launch; direct readers to the waitlist, not a signup or login.
- Cite specific curricula/frameworks accurately. Do not invent standards or assessment-objective mappings.

## Project commands

- `npm run dev` — local dev server
- `npm run build` — production build (also validates the content collection)
- `npx wrangler deploy` — deploy to Cloudflare (requires auth)

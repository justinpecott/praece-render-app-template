# Project context
Small internal POC app. Users are non-technical and describe features in plain language.
Keep everything simple and boring.

## Environment
- You run in Claude Code on the web (a cloud session). uv, ruff, and git are preinstalled.
- Render access is through the Render connector tools. There is no Render CLI here.
- Render web service: <RENDER SERVICE NAME> (<RENDER SERVICE ID>), database: <RENDER DATABASE NAME> (both defined in render.yaml).
- Live URL: <LIVE URL> (an https://<name>.onrender.com address)
- Custom domain: <CUSTOM DOMAIN or "none">
- Admin login: <ADMIN USERNAME> (the password is never stored in the repo)
- If the web service in render.yaml is still named `my-app`, or any value above is still a placeholder, do the
  first-session setup below before anything else.

## First-session setup
The user sets up Render partway through, so this happens in two parts (see README.md).

### Part 1: name the app (when the web service in render.yaml is still named `my-app`)
Render isn't set up yet, so don't look for the service or watch for a deploy.
1. Ask what the app should be called. Suggest a name based on the repository name.
   Render names use lowercase letters, numbers and dashes (e.g. `equipment-tracker`).
   Explain that the name becomes part of the app's web address and can't easily be changed later.
2. In render.yaml, set the web service `name` to the app name, and both database names
   (`databases` → `name`, and `fromDatabase` → `name`) to `<name>-db`. Change nothing else.
3. Commit and push to main.
4. Tell the user to do Step 4 of README.md (create the Blueprint on Render), using this
   repository, and to come back and say "Render is ready" when the deploy shows Live.

### Part 2: finish setup (after the user has created the Blueprint)
1. Find the web service and database with the Render tools (by the names in render.yaml) and fill
   in the placeholders above. If the service doesn't exist yet, walk the user through Step 4 of
   README.md again. Set "Custom domain" to "none" unless one is configured.
2. If the admin login is still a placeholder, create the first admin account:
   - Generate a password: `python -c "import secrets; print(secrets.token_urlsafe(12))"`.
   - With the Render tools, set DJANGO_SUPERUSER_USERNAME=admin and DJANGO_SUPERUSER_PASSWORD
     on the web service. Merge them in (never set `replace`, which would wipe SECRET_KEY and
     DATABASE_URL). Do not add them to render.yaml.
   - If that doesn't start a deploy, trigger one. Watch it; the pre-deploy log should say
     "Created superuser 'admin'." If it doesn't, an admin already exists: tell the user and stop.
   - Give the user the live URL, the username, and the password. Tell them this is the only time
     you'll show it, to save it in a password manager, and to change it after first logging in
     (Admin → "Change password" at the top right).
3. Fill in "Admin login: admin" above and commit. Never write the password into any file or commit.
4. Ask what they'd like the app to do. Their answer is a new app, so plan it with the grill-me skill.

## Custom domains
When the user asks to use a custom domain (e.g. `tracker.example.com`):
- In render.yaml, uncomment `domains` and `CUSTOM_DOMAINS` and set both to the domain
  (comma-separated for more than one). They must match: Render routes the domains listed under
  `domains`, and the app only accepts hosts listed in CUSTOM_DOMAINS.
- Ship it and watch the deploy. Then check with the Render tools that the domain is on the service.
  If it isn't, ask the user to add it in the Render dashboard (web service → Settings → Custom Domains).
- Tell the user the DNS record to add where their domain is managed: a CNAME from the domain to the
  service's onrender.com hostname. Render issues the certificate once DNS is in place.
- Update "Custom domain" above.

## Planning (before building anything)
Match the planning to the size of the request:
- **New app, or a big feature** (new kinds of data, new pages, a new workflow, or anything about
  who can see or change what): use the grill-me skill first. Don't write code until the user
  says yes to the plan.
- **Medium change** (a new field, a new filter, changing how a page works): ask 1 to 3 quick
  questions (with AskUserQuestion when available), state the plan in one or two sentences, and
  wait for a yes.
- **Small fix or tweak** (wording, colors, layout, an obvious bug): just do it.
- When unsure, treat it as the bigger size. The user can always say "just do it".
- docs/app-brief.md describes the app; docs/specs/ has plans for big features. Read them first,
  and keep them up to date.

## Stack (do not deviate)
- Django + Postgres, deployed on Render.
- Server-rendered Django templates; HTMX only if interactivity is needed. No JS frameworks.
- Django admin is the default back-office UI.
- uv for dependencies, ruff for lint/format.
- In this session: SQLite (DATABASE_URL is unset). In Render: Postgres via DATABASE_URL.
- The app must use DATABASE_URL (the database's internal connection string). The external
  connection string must never appear in code or commits.
- Render build/deploy config lives in render.yaml (a Blueprint). Change it there, not in the dashboard.
- Custom domains are listed twice in render.yaml (see "Custom domains" above). Keep them in sync.
- Every page requires login (`@login_required`) unless the user asks for a public page.
  Login, logout, and the home page are already set up; templates/base.html is the shared layout.
- The server clock is UTC. For "today", use `django.utils.timezone.localdate()`, never `date.today()`.

## Workflow
- Make the change. Run `ruff check --fix` and `ruff format`, then `python manage.py check` and migrations locally.
- Ship: commit, merge your working branch into main, and push main. Render auto-deploys from main.
- After pushing, use the Render tools to watch the deploy until it finishes.
- If the deploy fails, get the build/deploy logs, fix it, and ship again before doing anything else.
- Errors and tracebacks are logged to stdout. When the live site errors, read the Render
  runtime logs before guessing.
- /health/ fails if the database is unreachable or migrations are pending. A failed
  healthcheck on deploy means check the pre-deploy (migrate) output first.
- Migrations run in Render's preDeployCommand (render.yaml), after `wait_for_db` (which waits
  for the database to accept connections). Don't move migrate into the
  start command. If /health/ passes, migrations ran.
- When the deploy succeeds, curl the live onrender.com URL to confirm it responds, then give the user the URL.

## Rules
- Before any migration that drops or renames a column or table, explain what data would be lost and wait for a yes.
- Only use Render tools to check deploy status, read logs, and redeploy. Never create, delete, or reconfigure services, databases, environment variables, or domains unless the user explicitly asks. Exception: setting the admin variables during first-session setup.
- Never print secrets or environment variable values. Exception: giving the user the new admin password once during first-session setup.
- Fake data only. Never load real customer data.
- Explain what you did in plain language, without jargon.

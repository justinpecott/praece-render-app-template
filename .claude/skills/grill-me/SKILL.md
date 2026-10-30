---
name: grill-me
description: Interview the user about a new app or a big feature, one question at a time, then write a short plan and get their yes before building. Use for /grill-me, a new app, or any big feature.
---

# Grill me: plan before building

The user is not technical. Your job is to pull a clear, small, buildable plan out of their head
and get their yes before writing code. You are deciding WHAT to build with them; HOW is your job.

## How to ask

- Ask **one question at a time**. Wait for the answer before asking the next.
- Use the AskUserQuestion tool when it's available, so the user can click an answer: 2 to 4 options,
  your recommended one first and marked "(Recommended)". They can always type their own answer.
  If the tool isn't available, ask in plain text and include your suggested answer.
- Plain language, no jargon (say "things the app keeps track of", not "models"). If a term needs
  explaining, use an everyday example.
- **Never ask technical questions.** The stack is decided (see CLAUDE.md). Choose fields, pages,
  and code structure yourself.
- **Don't ask what you can look up.** Read the code, CLAUDE.md, and docs/ first.
- Push back on vague answers. "Track our stuff" → "What's one example of a thing you'd add? What do you write down about it today?"
- Ask for real examples (with made-up names). Examples reveal details, statuses and edge cases.
- Keep it small. This is a prototype. When something sounds like a later phase, say so and park it.
- Stop once you can describe the first version confidently: usually 8 to 15 questions for a new
  app, 3 to 6 for a big feature.

## What to find out

Skip anything already answered or already in docs/.

1. **The problem.** What are they doing today (spreadsheet, paper, email)? What goes wrong?
2. **The people.** Who uses it, and in what roles?
3. **Who can see and change what. Never skip this.** For each role: what can they see, add, edit,
   and delete? Is anything private to one person or team? Today, every logged-in user can see
   and change everything; say so, and ask whether that's OK.
4. **The things.** What does the app keep track of? For each: what details matter, and which are required?
5. **How things connect.** For example, each piece of equipment is at one location; a location has many.
6. **Statuses and rules.** Does anything move through stages (open → done)? What must never happen?
7. **What people do.** The 3 to 5 most common tasks, step by step.
8. **The first screen.** After logging in, what should someone see first? What needs attention?
9. **Search and lists.** How will they find things? By what filters?
10. **Dates and reminders.** Anything due, overdue, or recurring? What time zone are the users in?
11. **Out of scope.** What should this version deliberately NOT do?
12. **Demo data.** What would realistic fake data look like? How many of each thing?

For a big feature on an existing app, focus on 2, 3, 6, 7, and 11 as they apply to the feature.

## Write the plan

**New app:** write `docs/app-brief.md`:

- **Summary**: two or three sentences on what the app is for.
- **Users and permissions**: each role, and what it can see, add, edit, and delete.
- **What it tracks**: each thing, its details, and how things connect.
- **Rules**: statuses, required fields, things that must never happen.
- **Screens**: the home page and the main pages, one line each.
- **Not in the first version**: the parked ideas.
- **Build plan**: phases, each small enough to ship and check on its own. A typical shape:
  1. The things it tracks, editable in the admin, plus fake demo data.
  2. Pages to browse and search them.
  3. Forms for the common tasks.
  4. The home page dashboard.

**Big feature:** write `docs/specs/<short-feature-name>.md` with the same headings, trimmed to
what the feature needs, and update `docs/app-brief.md` if the feature changes it.

Show the user a plain-language summary (not the whole file) and ask:
"Does this match what you had in mind? Anything to add, remove, or change?"
Revise until they say yes.

## Then build

- Commit the plan.
- Build **one phase only**, following CLAUDE.md (check, ship, watch the deploy, check the live site).
- Fake demo data goes in a `load_demo_data` management command that only adds data when the
  database is empty. Add it to the end of `preDeployCommand` in render.yaml so the live site has data.
- When the phase is live, tell the user what to try, then ask whether to continue with the next one.
- Keep the plan files up to date as plans change.

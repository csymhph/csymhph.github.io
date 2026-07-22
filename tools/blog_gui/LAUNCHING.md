# Writing Studio Launching

## Entry points

- `blog-gui.command`: Finder double-click entrypoint.
- `scripts/open-blog-gui`: idempotent local launcher used by the command file
  and the macOS URL handler.
- `csymhph-blog://open`: exact custom URL accepted by the installed macOS
  launcher app.

All three routes reuse the same Streamlit server when it is already healthy.
Otherwise they start it on `http://127.0.0.1:8501` and open the browser after
the health endpoint responds.

## Install or refresh the web-link handler

Run from the repository root:

```bash
scripts/install-blog-gui-url-handler
```

The script builds and ad-hoc signs a small native launcher, installs it as
`~/Applications/Sangyeon Cho Writing Studio.app`, and registers the
`csymhph-blog` URL scheme with macOS Launch Services. If an installed launcher
already exists, the installer moves it to a timestamped backup before replacing
it.

The launcher stores the absolute repository launcher path, so rerun the install
script if the repository is moved.

## Publishing flow

1. Open the Writing Studio from Finder or an `csymhph-blog://open` link.
2. Create or edit a draft.
3. Publish the draft to `_posts`.
4. Open **Publish** in the Studio sidebar.
5. Select changed post files, review the commit message, confirm, and use
   **Commit and publish to website**.
6. GitHub Pages rebuilds from the pushed repository state.

## Security boundary

- Streamlit binds only to `127.0.0.1`; it is not a public editing server.
- The URL handler accepts only `csymhph-blog://open` with no parameters.
- The web page receives no filesystem access, Git credentials, secrets, or
  ability to choose commands.
- Git operations still run locally with the user's configured credentials and
  retain the Studio's explicit file selection and confirmation controls.
- On a Mac without the installed handler, the custom URL cannot open the
  Studio. On another device, use a separately designed authenticated hosted CMS
  instead of exposing this local Streamlit service.

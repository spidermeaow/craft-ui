# Craft UI Showcase

Native Windows component gallery for the **actual** public API of `packages/gui-template` 0.1.50. The app uses Craft Language, `packages/gui`, and `packages/gui-template`; all content is mock data. It does not read a database or call HTTP services.

## Run

From `D:\02-Repository\craft-ui`:

```powershell
craft package lock
craft check
craft test
craft run
```

If the installed CLI is older than 0.1.50, use `D:\02-Repository\craft\dist\craft.exe` in place of `craft`.

## What is shown

- **36 UiNode component APIs** are listed across Layout, Navigation, Buttons & Actions, Cards & Dashboard, Forms & Inputs, Data Display, and Responsive.
- **25 additional public helpers** (24 theme tokens plus `estimatedContentWidth`) are documented in [REGISTRY.md](REGISTRY.md).
- Feedback and Overlays show **Planned** because `gui-template` does not export those components yet.
- Each gallery card has a native live preview, the exact signature, an example call, supported variants and states, responsive notes, and limits. `shell` and `shellAdaptive` are demonstrated by the running application's root layout rather than nested windows.

The source is split into [application state and event loop](src/main.craft), [component registry](src/registry.craft), [native previews](src/previews.craft), and [gallery presentation](src/gallery.craft). [Registry generator](tools/generate_registry.py) reads the real package exports and produces the full API reference.

## Interaction guide

1. Select a sidebar category. The active item changes; the last event is shown above the gallery.
2. Use Search Components in the header on wide windows, or the page search field on compact windows. Search covers every component category.
3. Try button variants, disabled action, icon buttons, tabs, toggle, navigation items, form inputs, and **Change mock value** under `statCard`.
4. Resize the window across 1200, 900, and 650 logical px. The sidebar changes between expanded, compact and narrow modes. In narrow mode, use **Menu** to open it.
5. Try Windows display scales of 100%, 125%, and 150%. Check clipping, focus, scrolling, and form values. The app reports logical viewport width and layout mode on Overview.

This gallery is a **manual visual regression reference**, with stable IDs and repeatable mock data. It does not include an automated pixel-diff system. The template's narrow menu is a stacked panel, not a floating overlay. `splitButton` has adjacent actions but no popup. `toggleSwitch` is a button labeled On/Off. `formGrid` uses fields from `packages/gui`; the template itself has no form field components. `tableViewport` is a scroll wrapper, not a data table.

Reference captures from a Windows display at 125% scale are in [screenshots](screenshots): an expanded 1280×820 window and a narrow 640×480 window. These are visual aids, not proof of correct behavior at 100% or 150% scale.

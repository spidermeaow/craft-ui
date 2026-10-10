"""Generate the API registry from the real gui-template exports and showcase examples."""

from pathlib import Path
import re

project = Path(__file__).resolve().parents[1]
package = project.parent / "craft" / "packages" / "gui-template" / "src"
source = (project / "src" / "registry.craft").read_text(encoding="utf-8")

examples = {}
for line in source.splitlines():
    match = re.search(r'component\("([^"]+)", "([^"]+)", "([^"]+)", "([^"]+)", "(.*)"\),?$', line.strip())
    if match:
        name, category, description, signature, example = match.groups()
        examples[name] = (category, description, example.replace('\\"', '"'))

limited = {
    "splitButton", "toggleSwitch", "tableViewport", "formGrid", "shell",
    "shellAdaptive", "navigationWithStatus", "navigationCompact", "navItemState",
    "iconButtonState",
}
variants = {
    "actionButton": "primary / secondary / outline / danger; enabled / disabled",
    "statusBadge": "success / warning / danger / neutral",
    "statCard": "neutral / success / warning / danger; icon name or empty string",
    "shellAdaptive": "auto / expanded / collapsed; narrowOpen true / false",
    "navItemState": "normal / active / hovered",
    "iconButtonState": "normal / hovered / disabled",
}
states = {
    "actionButton": "ButtonPressed; native focus / pressed / disabled",
    "tabs": "ButtonPressed; selected index owned by caller",
    "toggleSwitch": "ButtonPressed; boolean owned by caller",
    "navItemState": "CanvasPressed and CanvasTargetEntered/Left; selected / hover owned by caller",
    "iconButtonState": "CanvasTargetPressed; hover owned by caller",
}
responsive = {
    "appHeaderAdaptive", "pageContainerResponsive", "formGrid", "metricGridResponsive",
    "shell", "shellAdaptive", "estimatedContentWidth", "layoutMode", "pagePadding",
}
limitations = {
    "splitButton": "Adjacent actions only; no popup.",
    "toggleSwitch": "Rendered as a button, not a native switch.",
    "tableViewport": "Scroll wrapper only; no template dataTable.",
    "formGrid": "Grid only; form fields come from packages/gui.",
    "shellAdaptive": "Narrow menu stacks; no overlay primitive.",
    "navigationCompact": "Five built-in icon names; no tooltip.",
    "navItemState": "No disabled navigation variant.",
    "iconButtonState": "No separate pressed visual.",
}

rows = []
for path in sorted(package.glob("*.craft")):
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"export func (\w+)\((.*?)\)(?:: (\w+))?", line)
        if not match:
            continue
        name, params, returns = match.groups()
        returns = returns or "Void"
        signature = f"{name}({params}): {returns}"
        category, description, example = examples.get(name, ("Design tokens / helpers", "Shared Enterprise Light design or layout helper.", ""))
        if not example:
            arguments = []
            for param in params.split(", ") if params else []:
                field, kind = param.split(": ", 1)
                arguments.append("1200" if kind == "Int" else "true" if kind == "Bool" else '"value"')
            example = f"template.{name}({', '.join(arguments)})"
        rows.append((name, category, description, signature, params or "none", "none in signature", variants.get(name, "single composition"), states.get(name, "caller owns state / no intrinsic interaction"), "width-aware; rebuild on resize" if name in responsive else "parent layout", example, "Limited" if name in limited else "Available", limitations.get(name, "See source for engine limits.")))

out = [
    "# Craft UI Showcase — Component Registry",
    "",
    "Generated from `../craft/packages/gui-template/src/*.craft` by `tools/generate_registry.py`.",
    f"Public API: **{len(rows)} functions**. UiNode components: **{len(examples)}**. Other theme/layout helpers: **{len(rows) - len(examples)}**.",
    "All parameters are required at the language signature level. An empty string or empty array may be used where the implementation treats content as optional.",
    "The app owns event handling and mutable state; the template creates UiNodes.",
    "",
    "| Component | Category | Status | Description | Signature | Required parameters | Optional parameters | Variants | States | Responsive | Example usage | Limitation |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|",
]
for row in rows:
    name, category, description, signature, required, optional, variant, state, behavior, example, status, limitation = row
    values = [f"`{name}`", category, status, description, f"`{signature}`", f"`{required}`", optional, variant, state, behavior, f"`{example}`", limitation]
    out.append("| " + " | ".join(value.replace("|", "\\|") for value in values) + " |")

out += [
    "",
    "## Planned / absent in 0.1.50",
    "",
    "`textField`, `numberField`, `selectField`, `searchField`, `checkboxField`, `radioGroup`, `dateField`, `dataTable`, `pagination`, `alertBanner`, `toast`, `modalDialog`, `confirmDialog`, `dropdownMenu`, `contextMenu`, and `tooltip` are **Planned**. They are not exported by this package and are not shown as working template components in the gallery.",
    "",
    "## Key event conventions",
    "",
    "Native buttons emit `ButtonPressed`. Tabs use IDs `<tabs-id>-<index>`. Canvas icon buttons emit `CanvasTargetPressed` on `<id>-target`. Navigation Canvas rows use their supplied node ID for `CanvasPressed`; hover can be driven by `CanvasTargetEntered` and `CanvasTargetLeft`. The caller updates state and calls `gui.update`.",
    "",
]
(project / "REGISTRY.md").write_text("\n".join(out), encoding="utf-8")
print(f"Generated {len(rows)} API rows ({len(examples)} UiNode components)")

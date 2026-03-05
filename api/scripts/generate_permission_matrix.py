from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HTTP_METHODS = {"get", "post", "put", "delete", "patch"}


@dataclass
class RouteRecord:
    module: str
    method: str
    path: str
    permission: str
    line: int


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan FastAPI views and generate permission matrix markdown.")
    parser.add_argument(
        "--api-dir",
        default="api",
        help="API package directory that contains module folders (default: api)",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output markdown file path. If omitted, print to stdout.",
    )
    return parser.parse_args()


def call_name(node: ast.AST | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        owner_name = call_name(node.value)
        return f"{owner_name}.{node.attr}" if owner_name else node.attr
    if isinstance(node, ast.Call):
        return call_name(node.func)
    return ""


def extract_route_path(decorator_call: ast.Call) -> str:
    if decorator_call.args and isinstance(decorator_call.args[0], ast.Constant) and isinstance(decorator_call.args[0].value, str):
        return decorator_call.args[0].value
    return ""


def extract_dep_targets_from_depends_call(node: ast.Call) -> str:
    if not node.args:
        return ""
    return call_name(node.args[0])


def collect_dependency_targets(function_node: ast.AsyncFunctionDef | ast.FunctionDef, decorator_call: ast.Call) -> list[str]:
    targets: list[str] = []

    for keyword in decorator_call.keywords:
        if keyword.arg != "dependencies" or not isinstance(keyword.value, ast.List):
            continue
        for item in keyword.value.elts:
            if isinstance(item, ast.Call) and call_name(item.func).endswith("Depends"):
                target_name = extract_dep_targets_from_depends_call(item)
                if target_name:
                    targets.append(target_name)

    for default_node in list(function_node.args.defaults) + [value for value in function_node.args.kw_defaults if value is not None]:
        if not isinstance(default_node, ast.Call):
            continue
        helper_name = call_name(default_node.func)
        if helper_name.endswith("Depends"):
            target_name = extract_dep_targets_from_depends_call(default_node)
            if target_name:
                targets.append(target_name)
        elif helper_name.endswith("Security"):
            target_name = extract_dep_targets_from_depends_call(default_node)
            if target_name:
                targets.append(target_name)

    return targets


def resolve_permission(dependency_targets: Iterable[str]) -> str:
    targets = list(dependency_targets)
    if any("get_current_super_user" in target for target in targets):
        return "Super"
    if any("get_current_user" in target for target in targets):
        return "Auth"
    if any("refresh_security" in target for target in targets):
        return "RefreshToken"
    return "Public"


def scan_view_file(file_path: Path, module_name: str) -> list[RouteRecord]:
    syntax_tree = ast.parse(file_path.read_text(encoding="utf-8"))
    routes: list[RouteRecord] = []

    for node in syntax_tree.body:
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Attribute):
                continue

            method_name = decorator.func.attr.lower()
            if method_name not in HTTP_METHODS:
                continue

            route_path = extract_route_path(decorator)
            dependency_targets = collect_dependency_targets(node, decorator)
            permission = resolve_permission(dependency_targets)

            routes.append(
                RouteRecord(
                    module=module_name,
                    method=method_name.upper(),
                    path=f"/api/{module_name}{route_path}",
                    permission=permission,
                    line=getattr(decorator, "lineno", getattr(node, "lineno", 0)),
                )
            )

    return sorted(routes, key=lambda record: record.line)


def collect_routes(api_dir: Path) -> dict[str, list[RouteRecord]]:
    module_to_routes: dict[str, list[RouteRecord]] = {}

    for view_file in sorted(api_dir.glob("*/views.py")):
        module_name = view_file.parent.name
        module_to_routes[module_name] = scan_view_file(view_file, module_name)

    return module_to_routes


def build_markdown(module_to_routes: dict[str, list[RouteRecord]]) -> str:
    lines: list[str] = []
    lines.append("# API 权限矩阵（自动生成草稿）")
    lines.append("")
    lines.append("- 统计范围：`api/api/*/views.py`")
    lines.append("- 权限推断规则：`get_current_super_user` > `get_current_user` > `refresh_security` > `Public`")
    lines.append("")

    for module_name, routes in module_to_routes.items():
        lines.append(f"## `api/{module_name}`")
        lines.append("")
        lines.append("| 方法 | 路径 | 权限 |")
        lines.append("|---|---|---|")
        for route in routes:
            lines.append(f"| {route.method} | `{route.path}` | `{route.permission}` |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    options = parse_arguments()
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    api_dir = (project_root / options.api_dir).resolve()

    if not api_dir.exists():
        raise SystemExit(f"api-dir not found: {api_dir}")

    module_to_routes = collect_routes(api_dir)
    markdown_content = build_markdown(module_to_routes)

    if options.output:
        output_path = (project_root / options.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content, encoding="utf-8")
        print(f"Written: {output_path}")
        return

    print(markdown_content)


if __name__ == "__main__":
    main()


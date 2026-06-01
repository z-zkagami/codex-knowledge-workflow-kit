#!/usr/bin/env bash
set -euo pipefail

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CN_ROOT="${CKW_VAULT_ROOT:-$WORKSPACE_ROOT/examples/demo-vault}"

if [[ ! -d "$CN_ROOT" ]]; then
  echo "ERROR: CN root not found: $CN_ROOT"
  exit 2
fi

missing_count=0
warn_count=0

print_header() {
  echo
  echo "== $1 =="
}

join_by_comma() {
  local IFS=","
  echo "$*"
}

check_research_layout() {
  print_header "30_研究"
  [[ -d "$CN_ROOT/30_研究" ]] || return 0
  local dir name
  while IFS= read -r -d '' dir; do
    name="$(basename "$dir")"
    local missing=()
    [[ -f "$dir/00_索引.md" ]] || missing+=("00_索引.md")
    [[ -d "$dir/_state" ]] || missing+=("_state/")
    [[ -d "$dir/sources" ]] || missing+=("sources/")
    [[ -d "$dir/notes" ]] || missing+=("notes/")
    [[ -d "$dir/assets" ]] || missing+=("assets/")

    if (( ${#missing[@]} == 0 )); then
      echo "OK       | $name"
    else
      echo "MISSING  | $name | $(join_by_comma "${missing[@]}")"
      ((missing_count+=1))
    fi
  done < <(find "$CN_ROOT/30_研究" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
}

check_wechat_layout() {
  print_header "60_内容中台/10_公众号"
  [[ -d "$CN_ROOT/60_内容中台/10_公众号" ]] || return 0
  local dir name
  while IFS= read -r -d '' dir; do
    name="$(basename "$dir")"
    local missing=()
    [[ -f "$dir/article.md" ]] || missing+=("article.md")
    [[ -d "$dir/_state" ]] || missing+=("_state/")
    [[ -d "$dir/drafts" ]] || missing+=("drafts/")
    [[ -d "$dir/sources" ]] || missing+=("sources/")
    [[ -d "$dir/assets" ]] || missing+=("assets/")
    [[ -d "$dir/build" ]] || missing+=("build/")
    [[ -d "$dir/publish" ]] || missing+=("publish/")

    local root_md_count
    root_md_count="$(find "$dir" -maxdepth 1 -type f -name '*.md' ! -name 'article.md' | wc -l | tr -d ' ')"

    if (( ${#missing[@]} == 0 )); then
      echo "OK       | $name | extra_root_md=$root_md_count"
    else
      echo "MISSING  | $name | $(join_by_comma "${missing[@]}") | extra_root_md=$root_md_count"
      ((missing_count+=1))
    fi
  done < <(find "$CN_ROOT/60_内容中台/10_公众号" -mindepth 2 -maxdepth 2 -type d -print0 | sort -z)
}

check_xhs_root_flatten() {
  print_header "60_内容中台/20_小红书"
  local xhs_root="$CN_ROOT/60_内容中台/20_小红书"
  [[ -d "$xhs_root" ]] || return 0
  local root_md_count
  root_md_count="$(find "$xhs_root" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"

  echo "INFO     | root_md_count=$root_md_count (new files should go to 素材池/)"
  if (( root_md_count > 0 )); then
    ((warn_count+=1))
  fi
}

check_resource_layout() {
  print_header "50_资源"
  local resources_root="$CN_ROOT/50_资源"
  local missing=()

  [[ -f "$resources_root/00_资源工作台.md" ]] || missing+=("00_资源工作台.md")
  [[ -d "$resources_root/Newsletters" ]] || missing+=("Newsletters/")
  [[ -d "$resources_root/信号简报" ]] || missing+=("信号简报/")
  [[ -d "$resources_root/风格参考" ]] || missing+=("风格参考/")
  [[ -d "$resources_root/临时收纳" ]] || missing+=("临时收纳/")

  if (( ${#missing[@]} == 0 )); then
    echo "OK       | 50_资源 base structure"
  else
    echo "MISSING  | 50_资源 | $(join_by_comma "${missing[@]}")"
    ((missing_count+=1))
  fi
}

check_local_venv() {
  print_header "Local venv scan (30_研究/50_资源/60_内容中台)"
  local found=0
  while IFS= read -r -d '' dir; do
    found=1
    echo "FOUND    | $dir"
  done < <(find "$CN_ROOT/30_研究" "$CN_ROOT/50_资源" "$CN_ROOT/60_内容中台" -type d \( -name 'venv' -o -name '.venv' \) -print0 2>/dev/null)

  if (( found == 0 )); then
    echo "OK       | no local venv/.venv"
  else
    ((missing_count+=1))
  fi
}

check_research_layout
check_wechat_layout
check_xhs_root_flatten
check_resource_layout
check_local_venv

echo
echo "== Summary =="
echo "missing_count=$missing_count"
echo "warn_count=$warn_count"
echo "strict_mode=$STRICT"

if (( missing_count > 0 )); then
  exit 1
fi

if (( STRICT == 1 && warn_count > 0 )); then
  exit 1
fi

exit 0

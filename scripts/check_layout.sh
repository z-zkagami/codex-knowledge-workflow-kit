#!/usr/bin/env bash
set -euo pipefail

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT_ROOT="${CKW_VAULT_ROOT:-$WORKSPACE_ROOT/examples/demo-vault}"

if [[ ! -d "$VAULT_ROOT" ]]; then
  echo "ERROR: Vault root not found: $VAULT_ROOT"
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
  print_header "30_Research"
  [[ -d "$VAULT_ROOT/30_Research" ]] || return 0
  local dir name
  while IFS= read -r -d '' dir; do
    name="$(basename "$dir")"
    local missing=()
    [[ -f "$dir/00_Index.md" ]] || missing+=("00_Index.md")
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
  done < <(find "$VAULT_ROOT/30_Research" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
}

check_wechat_layout() {
  print_header "60_Content/10_WeChat"
  [[ -d "$VAULT_ROOT/60_Content/10_WeChat" ]] || return 0
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
  done < <(find "$VAULT_ROOT/60_Content/10_WeChat" -mindepth 2 -maxdepth 2 -type d -print0 | sort -z)
}

check_xhs_root_flatten() {
  print_header "60_Content/20_Xiaohongshu"
  local xhs_root="$VAULT_ROOT/60_Content/20_Xiaohongshu"
  [[ -d "$xhs_root" ]] || return 0
  local root_md_count
  root_md_count="$(find "$xhs_root" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"

  echo "INFO     | root_md_count=$root_md_count (new files should go to Material_Pool/)"
  if (( root_md_count > 0 )); then
    ((warn_count+=1))
  fi
}

check_resource_layout() {
  print_header "50_Resources"
  local resources_root="$VAULT_ROOT/50_Resources"
  local missing=()

  [[ -f "$resources_root/00_Resources_Workbench.md" ]] || missing+=("00_Resources_Workbench.md")
  [[ -d "$resources_root/Newsletters" ]] || missing+=("Newsletters/")
  [[ -d "$resources_root/Signal_Briefs" ]] || missing+=("Signal_Briefs/")
  [[ -d "$resources_root/Style_References" ]] || missing+=("Style_References/")
  [[ -d "$resources_root/Staging" ]] || missing+=("Staging/")

  if (( ${#missing[@]} == 0 )); then
    echo "OK       | 50_Resources base structure"
  else
    echo "MISSING  | 50_Resources | $(join_by_comma "${missing[@]}")"
    ((missing_count+=1))
  fi
}

check_local_venv() {
  print_header "Local venv scan (30_Research/50_Resources/60_Content)"
  local found=0
  while IFS= read -r -d '' dir; do
    found=1
    echo "FOUND    | $dir"
  done < <(find "$VAULT_ROOT/30_Research" "$VAULT_ROOT/50_Resources" "$VAULT_ROOT/60_Content" -type d \( -name 'venv' -o -name '.venv' \) -print0 2>/dev/null)

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

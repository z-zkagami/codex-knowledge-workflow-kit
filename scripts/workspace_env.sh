#!/bin/bash
set -euo pipefail

PROJECT_SLUG="codex_knowledge_workflow_kit"
DATA_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/workspace-envs/$PROJECT_SLUG"
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}/workspace-envs/$PROJECT_SLUG"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/workspace-envs/$PROJECT_SLUG"
VENV_ROOT="$DATA_ROOT/venvs"
CONDA_ENV_ROOT="$DATA_ROOT/conda-envs"
TMP_ROOT="$CACHE_ROOT/tmp"
PYCACHE_ROOT="$CACHE_ROOT/pycache"

ensure_dirs() {
  mkdir -p \
    "$VENV_ROOT" \
    "$CONDA_ENV_ROOT" \
    "$CACHE_ROOT/uv" \
    "$CACHE_ROOT/pip" \
    "$CACHE_ROOT/pipenv" \
    "$CACHE_ROOT/pypoetry" \
    "$CACHE_ROOT/pdm" \
    "$CACHE_ROOT/conda-pkgs" \
    "$TMP_ROOT" \
    "$PYCACHE_ROOT" \
    "$STATE_ROOT"
}

default_python() {
  if [ -x "/opt/homebrew/bin/python3" ]; then
    echo "/opt/homebrew/bin/python3"
    return
  fi

  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return
  fi

  echo "python3"
}

print_exports() {
  ensure_dirs
  cat <<EOF
export CKW_ENV_ROOT="$DATA_ROOT"
export CKW_CACHE_ROOT="$CACHE_ROOT"
export CKW_STATE_ROOT="$STATE_ROOT"
export CKW_VENV_ROOT="$VENV_ROOT"
export CKW_CONDA_ENV_ROOT="$CONDA_ENV_ROOT"
export UV_CACHE_DIR="$CACHE_ROOT/uv"
export PIP_CACHE_DIR="$CACHE_ROOT/pip"
export PIPENV_CACHE_DIR="$CACHE_ROOT/pipenv"
export POETRY_CACHE_DIR="$CACHE_ROOT/pypoetry"
export POETRY_VIRTUALENVS_PATH="$VENV_ROOT"
export PDM_CACHE_DIR="$CACHE_ROOT/pdm"
export PDM_VENV_IN_PROJECT=0
export CONDA_PKGS_DIRS="$CACHE_ROOT/conda-pkgs"
export PYTHONPYCACHEPREFIX="$PYCACHE_ROOT"
export TMPDIR="$TMP_ROOT"
EOF
}

show_paths() {
  ensure_dirs
  cat <<EOF
项目标识: $PROJECT_SLUG
共享数据目录: $DATA_ROOT
共享缓存目录: $CACHE_ROOT
共享状态目录: $STATE_ROOT
虚拟环境目录: $VENV_ROOT
Conda 环境目录: $CONDA_ENV_ROOT
临时目录: $TMP_ROOT
字节码缓存目录: $PYCACHE_ROOT
EOF
}

list_envs() {
  ensure_dirs

  echo "[venv]"
  find "$VENV_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sort || true
  echo
  echo "[conda]"
  find "$CONDA_ENV_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sort || true
}

create_venv() {
  local env_name="${1:-codex-default}"
  local python_bin="${2:-$(default_python)}"
  local env_path="$VENV_ROOT/$env_name"

  ensure_dirs

  env \
    UV_CACHE_DIR="$CACHE_ROOT/uv" \
    PIP_CACHE_DIR="$CACHE_ROOT/pip" \
    PIPENV_CACHE_DIR="$CACHE_ROOT/pipenv" \
    POETRY_CACHE_DIR="$CACHE_ROOT/pypoetry" \
    POETRY_VIRTUALENVS_PATH="$VENV_ROOT" \
    PDM_CACHE_DIR="$CACHE_ROOT/pdm" \
    PDM_VENV_IN_PROJECT=0 \
    PYTHONPYCACHEPREFIX="$PYCACHE_ROOT" \
    TMPDIR="$TMP_ROOT" \
    uv venv "$env_path" --python "$python_bin"

  echo "已创建虚拟环境: $env_path"
  echo "激活命令: source \"$env_path/bin/activate\""
}

create_conda() {
  local env_name="${1:-codex-default}"
  local python_version="${2:-3.11}"
  local env_path="$CONDA_ENV_ROOT/$env_name"

  ensure_dirs

  env \
    CONDA_PKGS_DIRS="$CACHE_ROOT/conda-pkgs" \
    TMPDIR="$TMP_ROOT" \
    micromamba create -y -p "$env_path" "python=$python_version"

  echo "已创建 Conda 环境: $env_path"
  echo "激活命令: micromamba activate \"$env_path\""
}

remove_venv() {
  local env_name="${1:-}"

  if [ -z "$env_name" ]; then
    echo "请提供要删除的 venv 名称。" >&2
    exit 1
  fi

  local env_path="$VENV_ROOT/$env_name"

  if [ ! -d "$env_path" ]; then
    echo "未找到虚拟环境: $env_path" >&2
    exit 1
  fi

  rm -rf "$env_path"
  echo "已删除虚拟环境: $env_path"
}

remove_conda() {
  local env_name="${1:-}"

  if [ -z "$env_name" ]; then
    echo "请提供要删除的 Conda 环境名称。" >&2
    exit 1
  fi

  local env_path="$CONDA_ENV_ROOT/$env_name"

  if [ ! -d "$env_path" ]; then
    echo "未找到 Conda 环境: $env_path" >&2
    exit 1
  fi

  micromamba remove -y -p "$env_path" --all
  rm -rf "$env_path"
  echo "已删除 Conda 环境: $env_path"
}

doctor() {
  ensure_dirs

  echo "python3: $(command -v python3 || echo 未找到)"
  python3 --version 2>/dev/null || true
  echo "create-venv 默认解释器: $(default_python)"
  echo "uv: $(command -v uv || echo 未找到)"
  uv --version 2>/dev/null || true
  echo "micromamba: $(command -v micromamba || echo 未找到)"
  micromamba --version 2>/dev/null || true

  if command -v python3 >/dev/null 2>&1 && [[ "$(command -v python3)" == *"/anaconda3/"* ]]; then
    echo "提示: 当前 shell 仍然带着旧的 Anaconda PATH；新开一个登录 shell 后会恢复为 Homebrew Python。"
  fi

  echo
  show_paths
}

doctor_login_shell() {
  env -i \
    HOME="$HOME" \
    USER="${USER:-}" \
    SHELL=/bin/zsh \
    PATH=/usr/bin:/bin:/usr/sbin:/sbin \
    /bin/zsh -lic '
      echo "login shell python3: $(command -v python3 || echo 未找到)"
      python3 --version 2>/dev/null || true
      echo "login shell uv: $(command -v uv || echo 未找到)"
      uv --version 2>/dev/null || true
      echo "login shell micromamba: $(command -v micromamba || echo 未找到)"
      micromamba --version 2>/dev/null || true
      print -rl -- $path | rg "anaconda3|condabin" || true
    '
}

usage() {
  cat <<'EOF'
用法:
  bash scripts/workspace_env.sh exports
  bash scripts/workspace_env.sh show
  bash scripts/workspace_env.sh list
  bash scripts/workspace_env.sh doctor
  bash scripts/workspace_env.sh doctor-login-shell
  bash scripts/workspace_env.sh create-venv [环境名] [Python解释器]
  bash scripts/workspace_env.sh create-conda [环境名] [Python版本]
  bash scripts/workspace_env.sh remove-venv <环境名>
  bash scripts/workspace_env.sh remove-conda <环境名>

示例:
  eval "$(bash scripts/workspace_env.sh exports)"
  bash scripts/workspace_env.sh create-venv codex-docs python3
  bash scripts/workspace_env.sh create-conda codex-cuda 3.11
  bash scripts/workspace_env.sh list
  bash scripts/workspace_env.sh remove-venv codex-docs
EOF
}

command_name="${1:-help}"

case "$command_name" in
  exports)
    print_exports
    ;;
  show)
    show_paths
    ;;
  list)
    list_envs
    ;;
  doctor)
    doctor
    ;;
  doctor-login-shell)
    doctor_login_shell
    ;;
  create-venv)
    shift || true
    create_venv "${1:-codex-default}" "${2:-}"
    ;;
  create-conda)
    shift || true
    create_conda "${1:-codex-default}" "${2:-}"
    ;;
  remove-venv)
    shift || true
    remove_venv "${1:-}"
    ;;
  remove-conda)
    shift || true
    remove_conda "${1:-}"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    echo "未知命令: $command_name" >&2
    echo >&2
    usage >&2
    exit 1
    ;;
esac

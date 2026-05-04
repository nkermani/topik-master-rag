{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
    pkgs.git
  ];
  shellHook = ''
    echo "TOPIK Master RAG Development Shell (Python 3.12)"
    python --version

    # Auto-create and activate venv if not present
    if [ ! -d ".venv" ]; then
      echo "Creating virtual environment..."
      python -m venv .venv
    fi
    source .venv/bin/activate
    echo "Virtual environment activated. Run 'pip install -e .' to install deps."
  '';
}

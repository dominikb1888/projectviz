
{ pkgs ? import <nixpkgs> {} }:

let
  pythonPkgs = pkgs.python3Packages;
  myPackages = with pythonPkgs; [
    fastapi
    uvicorn
    requests
    python-dotenv

    jupyterlab
    ipython
    # Add more Python packages here as needed
  ];
in
pkgs.mkShell {
  name = "python-env";

  buildInputs = [
    pythonPkgs.python
    pythonPkgs.pip

  ] ++ myPackages;

  shellHook = ''
    export PYTHONPATH=$PYTHONPATH:${toString (builtins.head myPackages)}/lib/python3.*/site-packages
  '';
}


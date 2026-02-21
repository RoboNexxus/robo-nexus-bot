{ pkgs }: {
  deps = [
    pkgs.postgresql
    pkgs.libffi
    pkgs.openssl
    pkgs.python311
    pkgs.python311Packages.pip
  ];
}

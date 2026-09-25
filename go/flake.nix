{
  description = "A very basic flake";
  inputs = {
    nixpkgs.url = "https://channels.nixos.org/nixpkgs-unstable/nixexprs.tar.zst";
  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    {
      packages = builtins.mapAttrs (system: pkgs: {
        hello = pkgs.hello;

        default = inputs.self.packages.${system}.hello;
      }) inputs.nixpkgs.legacyPackages;

      devShells = builtins.mapAttrs (system: pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            go
            golangci-lint
            gopls
            delve

            wayland
            wayland-protocols
            libffi # oft
            libxkbcommon

            libGL

            # X11 fallbacks (usually required by GLFW)
            libX11
            libXcursor
            libXrandr
            libXinerama
            libXi
          ];
        };
      }) nixpkgs.legacyPackages;
    };
}

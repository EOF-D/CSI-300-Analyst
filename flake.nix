{
  description = "Development environment for CSI-300 Project 2";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = {
    self,
    nixpkgs,
    devenv,
    systems,
    ...
  } @ inputs: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
  in {
    packages = forEachSystem (system: {
      pkgs = nixpkgs.legacyPackages.${system};
      devenv-up = self.devShells.${system}.dev.config.procfileScript;
    });

    devShells = forEachSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      dev = devenv.lib.mkShell {
        inherit inputs pkgs;
        modules = [
          {
            packages = with pkgs; [
              zlib
              poetry
              python310
              libcxx
            ];

            enterShell = ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc
              ]}
            '';

            pre-commit.hooks = {
              black.enable = true;
              isort.enable = true;
              pyright.enable = true;
            };

            services.adminer.enable = true;

            services.mysql = {
              enable = true;
              package = pkgs.mysql80;
              initialDatabases = [
                {
                  name = "sakila";
                  schema = ./sakila-db/sakila-schema.sql;
                }
              ];

              ensureUsers = [
                {
                  name = "andy";
                  ensurePermissions = {
                    "sakila.*" = "ALL PRIVILEGES";
                  };
                }
              ];
            };
          }
        ];
      };
    });
  };
}

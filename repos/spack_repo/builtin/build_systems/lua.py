# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import (
    Builder,
    EnvironmentModifications,
    Executable,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    depends_on,
    extends,
    find,
    register_builder,
    when,
)


class LuaPackage(PackageBase):
    """Specialized class for lua packages"""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "LuaPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "lua"

    list_depth = 1  # LuaRocks requires at least one level of spidering to find versions

    build_system("lua")

    with when("build_system=lua"):
        depends_on("lua-lang")
        with when("^[virtuals=lua-lang] lua"):
            extends("lua")
        with when("^[virtuals=lua-lang] lua-luajit"):
            extends("lua-luajit+lualinks")
        with when("^[virtuals=lua-lang] lua-luajit-openresty"):
            extends("lua-luajit-openresty+lualinks")

@register_builder("lua")
class LuaBuilder(Builder):
    phases = ("unpack", "generate_luarocks_config", "preprocess", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("luarocks_args",)

    #: Names associated with package attributes in the old build-system format
    package_attributes = ()


from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import copy, export_conandata_patches, get
import os

required_conan_version = ">=1.55.0"


class VulkanUtilityLibrariesConan(ConanFile):
    name = "vulkan-utility-libraries"
    description = "Utility libraries for Vulkan developers."
    license = "Apache-2.0"
    topics = ("vulkan", "utility-libraries")
    homepage = "https://github.com/KhronosGroup/Vulkan-Utility-Libraries"
    url = "https://github.com/conan-io/conan-center-index"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False]
    }
    default_options = {
        "fPIC": True
    }

    @property
    def _min_cppstd(self):
        return "17"

    @property
    def _compilers_minimum_version(self):
        return {
            "17": {
                "apple-clang": "9",
                "clang": "6",
                "gcc": "7",
                "msvc": "191",
                "Visual Studio": "15.7",
            },
        }.get(self._min_cppstd, {})

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires(f"vulkan-headers/{self.version}", transitive_headers=True)

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.22.1 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        env = VirtualBuildEnv(self)
        env.generate()
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Vulkan"
        self.cpp_info.names["cmake_find_package_multi"] = "Vulkan"
        self.cpp_info.filenames["cmake_find_package"] = "VulkanUtilityLibraries"
        self.cpp_info.filenames["cmake_find_package_multi"] = "VulkanUtilityLibraries"
        self.cpp_info.set_property("cmake_file_name", "VulkanUtilityLibraries")
        self.cpp_info.libs = []
        self.cpp_info.components["vulkancompilerconfiguration"].names["cmake_find_package_multi"] = "CompilerConfiguration"
        self.cpp_info.components["vulkancompilerconfiguration"].names["cmake_find_package"] = "CompilerConfiguration"
        self.cpp_info.components["vulkancompilerconfiguration"].requires = ["vulkan-headers::vulkan-headers"]
        self.cpp_info.components["vulkancompilerconfiguration"].set_property("cmake_target_name", "Vulkan::CompilerConfiguration")
        self.cpp_info.components["vulkanlayersettings"].names["cmake_find_package_multi"] = "LayerSettings"
        self.cpp_info.components["vulkanlayersettings"].names["cmake_find_package"] = "LayerSettings"
        self.cpp_info.components["vulkanlayersettings"].libs = ["vulkanlayersettings"]
        self.cpp_info.components["vulkanlayersettings"].requires = ["vulkan-headers::vulkan-headers"]
        self.cpp_info.components["vulkanlayersettings"].set_property("cmake_target_name", "Vulkan::LayerSettings")
        self.cpp_info.components["vulkansafestruct"].names["cmake_find_package_multi"] = "SafeStruct"
        self.cpp_info.components["vulkansafestruct"].names["cmake_find_package"] = "SafeStruct"
        self.cpp_info.components["vulkansafestruct"].libs = ["vulkansafestruct"]
        self.cpp_info.components["vulkansafestruct"].requires = ["vulkan-headers::vulkan-headers"]
        self.cpp_info.components["vulkansafestruct"].set_property("cmake_target_name", "Vulkan::SafeStruct")
        self.cpp_info.components["vulkanutilityheaders"].names["cmake_find_package_multi"] = "UtilityHeaders"
        self.cpp_info.components["vulkanutilityheaders"].names["cmake_find_package"] = "UtilityHeaders"
        self.cpp_info.components["vulkanutilityheaders"].requires = ["vulkan-headers::vulkan-headers"]
        self.cpp_info.components["vulkanutilityheaders"].set_property("cmake_target_name", "Vulkan::UtilityHeaders")

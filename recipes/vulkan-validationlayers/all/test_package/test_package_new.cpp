// This header is no longer part of the validation layer package, which includes no headers.
#include <vulkan/utility/vk_format_utils.h>
#include <iostream>

int main() {
  std::cout << "VK_FORMAT_D16_UNORM " << (vkuFormatIsDepthOnly(VK_FORMAT_D16_UNORM) ? "is" : "is not") << " depth only" << std::endl;
  return 0;
}

#include <vulkan/utility/vk_format_utils.h>

#include <iostream>

int main() {
  return (int)!vkuFormatIsUNORM(VK_FORMAT_R4G4_UNORM_PACK8);
}

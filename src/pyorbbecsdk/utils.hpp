#include <pybind11/numpy.h>

#include <string>
#include <vector>

#define CHECK_NULLPTR(ptr)                                                  \
  do {                                                                      \
    if ((ptr) == nullptr) {                                                 \
      std::ostringstream oss;                                               \
      oss << "Null pointer exception in file " << __FILE__ << ", function " \
          << __FUNCTION__ << ", line " << __LINE__;                         \
      throw std::runtime_error(oss.str());                                  \
    }                                                                       \
  } while (false)

#define CHECK_LE(a, b)                                                        \
  if ((a) > (b)) {                                                            \
    std::ostringstream oss;                                                   \
    oss << "Invalid argument exception in file " << __FILE__ << ", function " \
        << __FUNCTION__ << ", line " << __LINE__;                             \
    throw std::invalid_argument(oss.str());                                   \
  }

#define CHECK_GE(a, b)                                               \
  do {                                                               \
    if ((a) < (b)) {                                                 \
      std::ostringstream oss;                                        \
      oss << "Invalid argument exception in file " << __FILE__       \
          << ", function " << __FUNCTION__ << ", line " << __LINE__; \
      throw std::invalid_argument(oss.str());                        \
    }                                                                \
  } while (false)

#define CHECK_NOT_EMPTY(str)                                                  \
  if ((str).empty()) {                                                        \
    std::ostringstream oss;                                                   \
    oss << "Invalid argument exception in file " << __FILE__ << ", function " \
        << __FUNCTION__ << ", line " << __LINE__;                             \
    throw std::invalid_argument(oss.str());                                   \
  }

namespace pyorbbecsdk {
std::vector<std::string> split(const std::string& s, const std::string& delim);
}

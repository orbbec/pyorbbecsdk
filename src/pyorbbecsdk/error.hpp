#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

#define OB_TRY_CATCH(code_block)         \
  do {                                   \
    try {                                \
      code_block                         \
    } catch (const ob::Error &error) {   \
      throw pyorbbecsdk::OBError(error); \
    }                                    \
  } while (false)

namespace pyorbbecsdk {

class OBError : public std::exception {
 public:
  OBError(std::string message, OBExceptionType type, std::string name,
          std::string args) noexcept
      : message_(std::move(message)),
        type_(type),
        name_(std::move(name)),
        args_(std::move(args)) {}

  explicit OBError(const ob::Error &error)
      : message_(error.getMessage()),
        type_(error.getExceptionType()),
        name_(error.getName()),
        args_(error.getArgs()) {}

  const char *what() const noexcept override { return message_.c_str(); }
  OBExceptionType get_type() const noexcept { return type_; }
  const char *get_name() const noexcept { return name_.c_str(); }

 private:
  std::string message_;
  OBExceptionType type_;
  std::string name_;
  std::string args_;
};

void define_orbbec_error(const py::object &m);
}  // namespace pyorbbecsdk

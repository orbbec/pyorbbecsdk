#include "error.hpp"

namespace pyorbbecsdk {

void define_orbbec_error(const py::object &m) {
  py::register_exception<OBError>(m, "OBError");
}
}  // namespace pyorbbecsdk

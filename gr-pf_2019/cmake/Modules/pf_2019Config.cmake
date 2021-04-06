INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PF_2019 pf_2019)

FIND_PATH(
    PF_2019_INCLUDE_DIRS
    NAMES pf_2019/api.h
    HINTS $ENV{PF_2019_DIR}/include
        ${PC_PF_2019_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PF_2019_LIBRARIES
    NAMES gnuradio-pf_2019
    HINTS $ENV{PF_2019_DIR}/lib
        ${PC_PF_2019_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/pf_2019Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PF_2019 DEFAULT_MSG PF_2019_LIBRARIES PF_2019_INCLUDE_DIRS)
MARK_AS_ADVANCED(PF_2019_LIBRARIES PF_2019_INCLUDE_DIRS)
